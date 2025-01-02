#!/usr/bin/python

# --- Day 9: Disk Fragmenter ---

import sys
import copy
from dataclasses import dataclass

# represents a single block on the disk
@dataclass
class Sector:
    is_file: bool
    ID: int

class SectorList:
    def __init__(self):
        self._sectors = []
    def append_count(self, s, count):
        for idx in range(count):
            self._sectors.append(s)
    def __iter__(self):
        return iter(self._sectors)
    def __reversed__(self):
        return reversed(self._sectors)
    def __len__(self):
        return len(self._sectors)
    def print_all(self):
        print(self._sectors)
    def swap(self, pos1, pos2):
        temp = copy.deepcopy(self._sectors[pos1])
        self._sectors[pos1] = copy.deepcopy(self._sectors[pos2])
        self._sectors[pos2] = copy.deepcopy(temp)
    def sanity_check(self):
        count = 0
        for s in self._sectors:
            if not s.is_file:
                break
            count += 1
        count2 = 0
        for s in reversed(self._sectors):
            if s.is_file:
                break
            count2 += 1
        print(f"Found {count} file blocks and {count2} empty blocks, total size {len(self._sectors)} blocks.")
        assert count + count2 == len(self._sectors)
    def checksum(self):
        checksum = 0
        for pos,s in enumerate(self._sectors):
            if not s.is_file:
                break
            checksum += pos * s.ID
        return checksum


def expand_disk_map(block_list):
    sector_is_file = True
    sector_ID = 0
    long_form = ""
    for b in block_list:
        s = Sector(sector_is_file, sector_ID)
        partition.append_count(s, b)
        if not sector_is_file:
            long_form += "." * b
        else:
            long_form += str(sector_ID) * b
            sector_ID += 1
        sector_is_file = not sector_is_file
    return long_form

def move_file_block():
    # find first empty sector
    for pos,e in enumerate(partition):
        if not e.is_file:
            break
    if pos == len(partition):
        raise RuntimeError("No space in partition.")
    # find last file
    for pos2,data in enumerate(reversed(partition)):
        if data.is_file:
            break
    pos2 = len(partition) - 1 - pos2
    if pos2 <= pos:
        # Compacting complete
        return False
    # swap the blocks
    partition.swap(pos, pos2)
    return True

# Create the partition map
partition = SectorList()

print("Read the disk partition")
file = open("input")
line = file.readline()
chars = list(line.rstrip())
numeric_data = [int(ch) for ch in chars]

file.close()

expand_disk_map(numeric_data)
#partition.print_all()
compact = True
loop = 0
while compact:
    compact = move_file_block()
    loop += 1
    if loop%1000 == 0:
        print(loop)
partition.sanity_check()
print(f"Checksum: {partition.checksum()}")

