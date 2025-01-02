#!/usr/bin/python

# --- Day 6: Guard Gallivant ---

import numpy as np
import copy
import sys

# right, down, left, up
directions = [[0,1], [1,0], [0,-1], [-1,0]]

def where_2d(arr, ch):
    # num rows, num columns
    dims = arr.shape
    found_list = []
    for y in range(dims[0]):
        for x in range(dims[1]):
            if arr[x, y] == ch:
                # row first!
                found_list.append([x,y])
    return found_list

class Maze:
    def __init__(self, arr):
        self._arr = arr
        self._pos = where_2d(arr, '^')[0] # guard position
        self._obs_list = where_2d(arr, "#")

    def set_direction(self, direction_idx):
        self._direction_idx = direction_idx
        self._direction = directions[direction_idx]

    def is_valid(self, pos):
        for i in range(2):
            if pos[i] < 0 or pos[i] >= self._arr.shape[i]:
                return False
        return True

    def visited(self, y0, x0, y1, x1):
        if x0 == x1:
            # include endpoints
            for y in range(y0, y1 + self._direction[0], self._direction[0]):
                self._arr[y,x0] = "X"
        else:
            for x in range(x0, x1 + self._direction[1], self._direction[1]):
                self._arr[y0,x] = "X"

    def print_slice(self, pos, size):
        dims = self._arr.shape
        y0 = max(0, pos[0] - size)
        y1 = min(pos[0] + size, dims[0])
        x0 = max(0, pos[1] - size)
        x1 = min(pos[1] + size, dims[1])
        print(self._arr[y0:y1,x0:x1])

    def find_obstacle(self):
        # scan along current direction
        t = [0,0]
        u = [0,0]
        for idx in range(2):
            t[idx] = self._pos[idx]
            u[idx] = self._pos[idx] + self._direction[idx]
        if not self.is_valid(u):
            # error, out of bounds
            raise IndexError("Invalid guard state")
        while self.is_valid(u):
            if self._arr[u[0], u[1]] == "#":
                return t
            for idx in range(2):
                t[idx] = u[idx]
                u[idx] = u[idx] + self._direction[idx]
        # No obstacle found
        return None


    def move_to_obstacle(self):
        pos = self._pos
        direction = self._direction
        print(f"Current pos: '{pos[0]}','{pos[1]}' and direction '{direction[0]}', '{direction[1]}'.")
        new_pos = self.find_obstacle()
        # Exit maze if no obstacle
        end = True if new_pos == None else False
        if end:
            new_pos = copy.deepcopy(self._pos)
            while self.is_valid(new_pos):
                for i in range(2):
                    new_pos[i] = new_pos[i] + self._direction[i]
            # FIXME
            for i in range(2):
                new_pos[i] = new_pos[i] - self._direction[i]
        # Update visited array
        self.visited(pos[0], pos[1], new_pos[0], new_pos[1])
        # Update position and direction
        self.set_direction( (self._direction_idx + 1) % 4 )
        self._pos = new_pos
        self.print_slice(self._pos, 6)
        #print("New position:", new_pos)
        return end


print("Read the array/map")
file = open("input")
wordsearch= []
for line in file:
    chars = list(line.rstrip())
    if len(chars) > 0:
        wordsearch.append(chars)
file.close()

y = np.array(wordsearch)

guard = where_2d(y, '^')[0]
print(f"Row '{guard[0]}', Column '{guard[1]}'")

# Create the maze/lab
lab = Maze(y)
lab.set_direction(3) # 'up'
while True:
    end = lab.move_to_obstacle()
    if end:
        break

ans = len(where_2d(lab._arr, "X"))
print(f"Visited '{ans}' squares.");

#np.set_printoptions(threshold=sys.maxsize)
#print(lab._arr)
