#!/usr/bin/python

# --- Day 10: Hoof It ---

import re
import sys
from itertools import chain


# Represents a square on the map, with valid hiking trails
# from the square, i.e. the height is exactly 1 greater than
# the current height, moving horizontally or vertically.
class Node:
    def __init__(self, x, y, height):
        self._height = height
        self._next_trail = []
        self._x = x
        self._y = y
        # visited end-points
        self._visited = False

    def __repr__(self):
        return f"Node({self._x}, {self._y}, {self._height}, {self._visited})"

    def add_neighbour(self, node):
        self._next_trail.append(node)

    def __iter__(self):
        # Use the itertools 'chain' to chain together the child iterators
        # Trail change in height condition already met below
        # NOTE: Python3 map supports iterators, no need for 'imap'
        #print(self._x, self._y, self._height)
        self._visited = True
        yield self
        for v in self._next_trail:
            for node in v:
                yield node



def is_valid(x,y):
    if y >= 0 and y < len(hiking_map) and x >= 0 and x < len(hiking_map[0]):
        # check whether square is passable
        if hiking_map[y][x] >= 0:
            return True
    return False

# UP, LEFT, DOWN, RIGHT
directions = ((0,1), (-1,0), (0,-1), (1,0))

def find(x, y):
    for node in nodes:
        if node._x == x and node._y == y:
            return node
    return None

# check and add neighbours
def add_neighbours(node0):
    x = node0._x
    y = node0._y
    h0 = node0._height
    for d in directions:
        x2 = x + d[0]
        y2 = y + d[1]
        if is_valid(x2, y2):
            h = hiking_map[y2][x2]
            if h == h0 + 1:
                node = find(x2, y2)
                if node is None:
                    raise RuntimeError("Node does not exist.")
                node0.add_neighbour(node)

# create tree
def create_tree():
    for y in range(len(hiking_map)):
        for x in range(len(hiking_map[0])):
            if not is_valid(x, y):
                continue
            current_height = hiking_map[y][x]
            node = Node(x, y, current_height)
            nodes.append(node)
            if current_height == 0:
                trailheads.append(node)
    for node in nodes:
        add_neighbours(node)

# traverse the tree
def count_trails():
    total_score = 0
    for th in trailheads:
        x = list(iter(th))
        summits = [n for n in nodes if n._visited and n._height == 9]
        score = len(summits)
        print(th, score)
        total_score += score
        # reset visited state
        for n in nodes:
            n._visited = False
    return total_score

# Read map
print("Reading the map file")
file = open("input")

hiking_map= []
nodes = []
trailheads = [] # Squares with height 0

for line in file:
    chars = list(line.rstrip())
    numeric = list()
    if len(chars) == 0:
        continue
    for ch in chars:
        if ch == ".":
            n = -1 # impassable terrain
        else:
            n = int(ch)
        numeric.append(n)
    hiking_map.append(numeric)
file.close()

# Create the tree
print("Build tree")
create_tree()

#print("Traverse the tree")
score = count_trails()
print("Score: %d" % score)
