#!/usr/bin/python

# --- Day 8: Resonant Collinearity ---

import sys
import re
from dataclasses import dataclass
from itertools import combinations

@dataclass
class Coord:
    x: int
    y: int

# return difference
def calc_antinode(c1, c2):
    return Coord(2*c1.x - c2.x, 2*c1.y - c2.y)

def add(c1, c2):
    return Coord(c1.x + c2.x, c1.y + c2.y)


class Antennas:
    def __init__(self):
        self._antennas = dict()
        self._antinodes = []

    def add(self, ch, loc):
        if ch in self._antennas.keys():
            self._antennas[ch].append(loc)
        else:
            self._antennas[ch] = [loc]

    def parse_map(self, map_ant):
        self._ymax = len(map_ant)
        self._xmax = len(map_ant[0])
        self._map_ant = map_ant
        for yc in range(self._ymax):
            for xc in range(self._xmax):
                ch = map_ant[yc][xc]
                m = re.match("[a-zA-Z0-9]{1}", ch)
                if m:
                    loc = Coord(xc,yc)
                    self.add(ch, loc)

    def add_antinode(self, c):
        if c.x >= 0 and c.x < self._xmax and c.y >= 0 and c.y < self._ymax:
            if c not in self._antinodes:
                self._antinodes.append(c)

    def find_antinodes(self):
        # find pairs of antennae, and the taxi-distance between them
        for k, coords in self._antennas.items():
            if len(coords) == 1:
                continue
            for pairs in combinations(coords, 2):
                c1 = pairs[0]
                c2 = pairs[1]
                self.add_antinode(calc_antinode(c1, c2))
                self.add_antinode(calc_antinode(c2, c1))

    def print_map(self):
        total = len(self._antinodes)
        print("Total number of unique antinodes: %d" % total)
        for node in self._antinodes:
            self._map_ant[node.y][node.x] = "#"
        for row in self._map_ant:
            print("".join(row))


# Read the map
ant_map = []
with open("input", "r") as f:
    for line in  f:
        line2 = line.rstrip()
        if len(line2) == 0:
            continue
        ant_map.append(list(line2))

ant = Antennas()
ant.parse_map(ant_map)
print(ant._antennas)

ant.find_antinodes()
ant.print_map()

