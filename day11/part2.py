#!/usr/bin/python

import sys
from itertools import chain

class Node:
    def __init__(self, value):
        self._value = value
        self._level = 0          # updated when child is added
        self._enable = True
        self._top = None         # top-most node for repeating nodes
        self._subnodes = []      # list of recurring nodes with equal value
        self._child_count = []   # child count at specified depth (recursive, cached)
        self._children = []

    def __repr__(self):
        return str(self._value)

    def add(self, child):
        self._children.append(child)
        child._level = self._level + 1

    def __iter__(self):
        yield self
        for v in chain(*map(iter, self._children)):
            yield v

    def print_tree(self):
        for t in self:
            indent = "-" * t._level
            if t._enable:
                print(f"{indent}Node({t._value}): en={t._enable}, child_count={t._child_count}")
            else:
                print(f"{indent}Node({t._value}): top->{t._top._value}")

    def accumulate_marker(self, level):
        top = self._top
        num_levels = level - self._level
        assert (num_levels >= 0)
        if num_levels < 1:
            # no children yet
            return
        idx = num_levels - 1 # offset into child count list
        if len(top._child_count) == 0:
            print(f"An error occurred at {top._value} (enable={top._enable}) with level {top._level}/{level}. Trying subnodes:")
            for n in top._subnodes:
                l = len(n._child_count)
                print(f"Node {n._value} (enable={top._enable}) with level {n._level}/{level}, child count {l}.")
            pebbles._tree[0].print_tree()
            root = pebbles._tree[7]
            root.print_tree()
            sys.exit(1)
        try:
            #print(top, level, top._level, idx)
            #print(top._subnodes)
            #print(top._enable)
            num_children = top._child_count[idx]
            self._child_count.append(num_children)
        except IndexError:
            raise IndexError(f"Child count {top._value} with data {top._child_count} at index {idx} is not ready.")

    def accumulate(self, level):
        # recurse n levels, counting nodes at each level
        # pass 1: count children
        # pass 2: count grandchildren
        # pass 3: count great-grandchildren, etc
        # keep historical counts for use in the Marker class
        if not self._enable:
            self.accumulate_marker(level)
            return

        #print(f"Accumulate: {self._value}, level={self._level}, children={self._children}")
        if level - self._level == 1:
            self._child_count.append(len(self._children))
        elif level - self._level >= 2:
            try:
                for v in self._children:
                    v.accumulate(level)
                s = sum(v._child_count[-1] for v in self._children)
                self._child_count.append(s)
            except IndexError:
                raise IndexError(f"At {self._value} with level {self._level}/{level}, has no data.")

    def find_by_value(self, v):
        if self._value == v:
            return self
        for c in self._children:
            if c._enable:
                return c.find_by_value(v)
        return None

# marker state, with propagation rule which increments its 'age'
# TODO: propagation rule descends the existing tree and updates
# the partial count, following other markers where they exist.

class Marker:
    def __init__(self, s):
        self._stone = s
        self._age = 0
        self._tree = list(pebbles._tree)

    def __repr__(self):
        return f"S_{self._stone}({self._age})"

    def __len__(self):
        n = self._tree.find_by_value(self._stone)
        if n is None:
            print(f"Warning: {self._stone} not found!")
            return 0
        return n.count(self._age)

    def next_blink(self):
        self._age += 1

class State:
    def __init__(self, init_state):
        self._stones = list(map(int, init_state.split()))
        self._blink_count = 0
        self._deferred_list = []
        self._marker_list = []
        self._tree = [Node(v) for v in self._stones]
        self._node_dict = dict()
        for x in zip(self._stones, self._tree):
            self._node_dict[x[0]] = x[1]

    def __len__(self):
        count = 0
        for s in self._stones:
            if type(s) is int:
                count += 1
            elif type(s) is Marker:
                # delegate count to the marker
                count += len(s)
            else:
                raise RuntimeError(f"Unknown stone type at {s}")
        return count

    def add_child(self, parent, child):
        # parent node already exists
        parent_node = self._node_dict[parent]
        #print(f"add_child: {parent}, {child}")
        child_node = Node(child)
        if child in self._node_dict.keys():
            top = self._node_dict[child]
            child_node._top = top
            top._subnodes.append(child_node)
            child_node._enable = False
            # NOTE: child_node is not in dictionary. This is intentional!
        else:
            #print(f"Adding new node {child} with parent {parent}.")
            self._node_dict[child] = child_node
        parent_node.add(child_node)

    def prune(self):
        # Disable recurring stones to save computational effort
        # NOTE: no longer used. The dictionary is already updated so
        # pruning here can lose track of active stones.
        try:
            for e, s in enumerate(self._stones):
                if type(s) is Marker:
                    continue
                node = self._node_dict[s]
                if node._level < self._blink_count:
                    # stone is historical, prune/disable current copy
                    self._stones[e] = Marker(s)
        except KeyError:
            raise KeyError(f"Key {s} not found in dictionary!")

    def check_create_marker(self, stone):
        if stone in self._node_dict.keys():
            m = Marker(stone)
            self._marker_list.append(m)
            return m
        else:
            return stone # integer ID

    def rule1(self, stone, idx):
        if stone == 0:
            self._stones[idx] = self.check_create_marker(1)
            self.add_child(0, 1)
            return True
        return False

    # defer the insertions to ensure the new stones are not modified
    def defer_insert(self, idx, stone):
        self._deferred_list.append( (idx, stone) )

    def run_deferred(self):
        # reverse the list to avoid modifying the offsets of
        # subsequent insertions at the front of the list
        for p in reversed(self._deferred_list):
            self._stones.insert(p[0], p[1])
        self._deferred_list.clear()

    def rule2(self, stone, idx):
        if len(str(stone)) % 2 == 0:
            s = str(stone)
            n = len(s)
            string1 = s[0:n//2]
            string2 = s[n//2:]
            stone1 = int(string1)
            self._stones[idx] = self.check_create_marker(stone1)
            self.add_child(stone, stone1)
            stone2 = int(string2)
            self.defer_insert(idx+1, self.check_create_marker(stone2))
            # add child node as the stone split in two
            self.add_child(stone, stone2)
            return True
        return False

    def rule3(self, stone, idx):
        self._stones[idx] = self.check_create_marker(stone * 2024)
        self.add_child(stone, stone * 2024)
        return True

    def next_blink(self):
        self._blink_count += 1
        for e, s in enumerate(self._stones):
            if type(s) is Marker:
                # subgraph, terminate calculation
                s.next_blink()
                continue
            if self.rule1(s, e):
                continue
            elif self.rule2(s, e):
                continue
            else:
                self.rule3(s, e)
        self.run_deferred()
        #self.prune()
        # count child nodes
        for t in self._tree:
            t.accumulate(self._blink_count)

    def print(self):
        print(f"\n\nAfter {self._blink_count} blinks:")
        print(self._stones)



def sanity_check():
    # Add up the counts for the final stones/markers
    count = 0
    for s in pebbles._stones:
        if type(s) is int:
            count += 1
        else:
            stone = s._stone
            age = s._age
            top = pebbles._node_dict[stone] # active stone
            if age == 0:
                marker_count = 1
            else:
                print(f"Check {stone}, age={age}, child_count={top._child_count}")
                marker_count = top._child_count[age - 1]
            count += marker_count
    count2 = sum(t._child_count[-1] for t in pebbles._tree)
    print(f"Total count from final state: {count}, from tree: {count2}")
    assert(count == count2)

# Read the initial state
file = open("input")
line = file.readline()
line = line.rstrip()

# Lookup table for stones to avoid repeating the calculation,
# neighbouring stones do not interact.
# Data format: <stone> -> list of number of stones after N blinks
# Eg. [0] -> [1, 1, 2, 4]

#pebbles = State("1")
pebbles = State(line)
num_blinks = 75
for blink in range(num_blinks):
    pebbles.next_blink()
    #pebbles.print()
#pebbles._tree[0].print_tree()

#print(f"After {num_blinks} blinks there are {len(pebbles)} stones.")
sanity_check()


