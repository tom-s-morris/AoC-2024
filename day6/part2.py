#!/usr/bin/python

import numpy as np
import copy
import sys

# right, down, left, up
directions = ((0,1), (1,0), (0,-1), (-1,0))

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

class State:
    def __init__(self, pos, direction_idx):
        self._pos = pos
        self._direction_idx = direction_idx
        self._visited = [(pos[0], pos[1], direction_idx)]

    def append(self, node):
        self._visited.append(node)

    def is_repeat(self, node):
        return node in self._visited

    def reset(self):
        start = copy.deepcopy(self._visited.pop(0))
        self._visited.clear();
        self._visited.append(start)
        return start

class Maze:
    def __init__(self, arr, direction_idx):
        self._arr = arr
        self._pos = where_2d(arr, '^')[0] # guard position
        self.set_direction(direction_idx)
        self._stop = False
        # List of visited positions/direction (UP)
        self._history = State(self._pos, direction_idx)

    def set_direction(self, direction_idx):
        self._direction_idx = direction_idx
        self._direction = directions[direction_idx]

    def reset(self):
        # Reset state for next solution
        start_state = self._history.reset()
        # Copy values!
        self._pos[0] = start_state[0]
        self._pos[1] = start_state[1]
        self.set_direction(start_state[2])
        self._stop = False
        try:
            self.unset_obstruction()
        except AttributeError:
            return

    def stopped(self):
        return self._stop

    def set_obstruction(self, pos):
        if self._arr[pos] == '#' or self._arr[pos] == '^':
            return False
        self._obstruction = pos
        self._arr[pos] = 'O'
        return True

    def unset_obstruction(self):
        self._arr[self._obstruction] = '.'
        del self._obstruction

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
            self.print_slice(u, 10)
            raise IndexError("Invalid guard state")
            #return None
        while self.is_valid(u):
            if self._arr[u[0], u[1]] == "#" or self._arr[u[0], u[1]] == "O":
                return t
            for idx in range(2):
                t[idx] = u[idx]
                u[idx] = u[idx] + self._direction[idx]
        # No obstacle found
        return None

    def add_node(self, new_pos):
        node = (new_pos[0], new_pos[1], self._direction_idx)
        if self._history.is_repeat(node):
            self._stop = True
            #raise RuntimeError(f"Cycle found at '{new_pos[0]}','{new_pos[1]}'")
        self._history.append(node)

    def move_to_obstacle(self):
        pos = self._pos
        direction = self._direction
        #print(f"Current pos: '{pos[0]}','{pos[1]}' and direction '{direction[0]}', '{direction[1]}'.")
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
        #self.visited(pos[0], pos[1], new_pos[0], new_pos[1])

        # Update position and direction
        self.set_direction( (self._direction_idx + 1) % 4 )
        self._pos = new_pos
        # Track visited nodes and look for cycle
        self.add_node(new_pos)
        #self.print_slice(self._pos, 6)
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
lab = Maze(y,3) # 'up'


def test(p):
    if not lab.set_obstruction(p):
        return
    success = False
    while True:
        end = lab.move_to_obstacle()
        if end:
            break
        if lab.stopped():
            print("[%3d] Guard in loop!" % (count))
            success = True
            break
    lab.reset()
    return success

count = 0
dims = lab._arr.shape
for y in range(dims[0]):
    for x in range(dims[1]):
        if test((x,y)):
            count += 1
print("Number of positions: %d" % count)
