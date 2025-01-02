#!/usr/bin/python

# --- Day 4: Ceres Search ---

import numpy as np


directions = [[1,0], [0,1], [-1,0], [0,-1],
        [1,1], [-1,1], [-1,-1], [1,-1]]

def where_2d(arr, ch):
    dims = arr.shape
    found_list = []
    for y in range(dims[1]):
        for x in range(dims[0]):
            if arr[x, y] == ch:
                found_list.append([x,y])
    return found_list

def word_search(arr, word, direction):
    word2 = list(word)
    dims = arr.shape
    matches = 0
    for p in where_2d(arr, 'X'):
        #print(p)
        c = 0
        m = True
        for ch in word2:
            sx = p[0] + c*direction[0]
            if sx < 0 or sx >= dims[1]:
                # row limit reached
                m = False
                break
            sy = p[1] + c*direction[1]
            if sy < 0 or sy >= dims[0]:
                # column limit reached
                m = False
                break
            if ch != arr[sx,sy]:
                m = False
                break
            c = c + 1
        # Found a match
        if m:
            matches = matches + 1
    return matches


print("Read the array/wordsearch")
file = open("input")
wordsearch = []
for line in file:
    chars = list(line.rstrip())
    if len(chars) > 0:
        wordsearch.append(chars)
file.close()

y = np.array(wordsearch)

print(y)
print(y[0,8])

num_matches = 0
for d in directions:
    num_matches = num_matches + word_search(y, "XMAS", d)
print("Found %d matches" % num_matches)
