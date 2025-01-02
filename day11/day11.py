#!/usr/bin/python

# --- Day 11: Plutonian Pebbles ---
# NOTE: has the outline of a tree structure for part 2.

import sys
from itertools import chain

class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def add(self, child):
        self._children.append(child)

    def __iter__(self):
        yield self
        for v in chain(*map(iter, self._children)):
            yield v

    def find_by_value(self, v):
        it = iter(self)
        while it:
            if next(it)._value = v:
                return next(it)
            it = next(it)
        return None

class State:
    def __init__(self, init_state):
        self._stones = list(map(int, init_state.split()))
        self._blink_count = 0
        self._deferred_list = []
        self._tree = [Node(v) for v in self._stones]
        self._node_dict = dict()
        for x in zip(self._stones, self._tree):
            self._node_dict[x[0]] = x[1]

    def add_child(self, parent, child):
        # parent node already exists
        parent_node = self._node_dict[parent]
        if num_child in self._node_dict.keys():
            child_node = self._node_dict[child]
        else:
            child_node = Node(child)
        parent_node.add(child_node)
        # NOTE: ** stones list will be optimised/pruned later **

    def rule1(self, stone, idx):
        if stone == 0:
            self._stones[idx] = 1 # ints are immutable
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
            self._stones[idx] = stone1
            stone2 = int(string2)
            self.defer_insert(idx+1, stone2)
            # add two child nodes as the stone split in two
            self.add_child(stone, stone1)
            self.add_child(stone, stone2)
            return True
        return False

    def rule3(self, stone, idx):
        self._stones[idx] = stone * 2024
        self.add_child(stone, stone * 2024)
        return True

    def next_blink(self):
        self._blink_count += 1
        for e, s in enumerate(self._stones):
            if self.rule1(s, e):
                continue
            elif self.rule2(s, e):
                continue
            else:
                self.rule3(s, e)
        self.run_deferred()

    def print(self):
        print(f"After {self._blink_count} blinks:")
        print(self._stones)

# Read the initial state
file = open("test3")
line = file.readline()
line = line.rstrip()

# Lookup table for stones to avoid repeating the calculation,
# neighbouring stones do not interact.
# Data format: <stone> -> list of number of stones after N blinks
# Eg. [0] -> [1, 1, 2, 4]

pebbles = State("1")
num_blinks = 6
for blink in range(num_blinks):
    pebbles.next_blink()
    pebbles.print()

print(f"After {num_blinks} blinks there are {len(pebbles._stones)} stones.")

for t in pebbles._tree:
    print(t._value)

