#!/usr/bin/python

import sys
import copy
from dataclasses import dataclass

# represents a single block on the disk
@dataclass
class Sector:
    is_file: bool
    ID: int

# represents a file, must be contiguous
@dataclass
class File:
    start_pos: int
    length: int

class SectorList:
    def __init__(self):
        self._sectors = []
        self._files = []
    def append_count(self, s, count):
        for idx in range(count):
            self._sectors.append(s)
        if s.is_file:
            f = File(len(self._sectors) - count, count)
            self._files.append(f)
    def __iter__(self):
        return iter(self._sectors)
    def __reversed__(self):
        return reversed(self._sectors)
    def __len__(self):
        return len(self._sectors)
    def print2(self):
        l = []
        for s in self._sectors:
            if s.is_file:
                l.append(str(s.ID))
            else:
                l.append(".")        
        print( ''.join(l) )

    def print_all(self):
        print(self._sectors)
    def swap(self, pos1, pos2):
        temp = copy.deepcopy(self._sectors[pos1])
        self._sectors[pos1] = copy.deepcopy(self._sectors[pos2])
        self._sectors[pos2] = copy.deepcopy(temp)
    def move_file(self, f, new_pos):
        # length is unchanged
        self._file[f].start_pos = new_pos

    def sanity_check(self):
        count = 0
        for s in self._sectors:
            if s.is_file:
                count += 1
        count2 = 0
        for s in reversed(self._sectors):
            if not s.is_file:
                count2 += 1
        print(f"Found {count} file blocks and {count2} empty blocks, total size {len(self._sectors)} blocks.")
        assert count + count2 == len(self._sectors)
    def checksum(self):
        checksum = 0
        for pos,s in enumerate(self._sectors):
            if s.is_file:
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

def move_file(f):
    span = 0
    is_space = False
    # find an empty sector which is large enough
    for pos,e in enumerate(partition):
        # stop when the file can no longer move to the left
        if pos > f.start_pos:
            return False
        if e.is_file:
            # reset span
            span = 0
        else:
            span += 1
        if span == f.length:
            pos -= (span - 1)
            is_space = True
            break
    if not is_space:
        return False

    # space available, update partition
    for s in range(f.length):
        partition.swap(pos + s, f.start_pos + s)
    f.start_pos = pos
    return True

def compact():
    for loop,f in enumerate(reversed(partition._files)):
        if loop%1000 == 0:
            print(loop)
        move_file(f)



# Create the partition map
partition = SectorList()

print("Read the disk partition")
file = open("input")
line = file.readline()
chars = list(line.rstrip())
numeric_data = [int(ch) for ch in chars]

file.close()

# Process the partition
expand_disk_map(numeric_data)
compact()
partition.sanity_check()
print(f"Checksum: {partition.checksum()}")

