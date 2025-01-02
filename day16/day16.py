#!/usr/bin/python

# --- Day 16: Reindeer Maze ---

import sys
import re
from dataclasses import dataclass


# represents a single location in the maze
@dataclass
class Point:
    x: int
    y: int


# The Maze is delineated with '#' for walls, 'S' for start and 'E' for end.
# All other squares should be marked '.'
# The reindeer starts facing East.
# Scoring: 1 point per tile, 1000 points per turn by +/- 90 degrees
# The objective is to find the path with the *lowest score*.
class Maze:
    def __init__(self, data):
        self._data = data
        # (number of columns, number of rows)
        self._size = Point(len(data[0]), len(data))
        self.parse()

    def parse(self):
        self._start = self.find_pt("S")
        print(self._start)
        self._end = self.find_pt("E")

    def find_pt(self, char):
        for y in range(self._size.y):
            for x in range(self._size.x):
                if self._data[y][x] == char:
                    return Point(x,y)
        return None

def read_file(name):
    file = open(name, "r")
    data = list()
    for line in file:
        chars = list(line.rstrip())
        if len(chars) == 0:
            continue
        data.append(chars)
    file.close()
    return data

map_data = read_file("test")
maze1 = Maze(map_data)

