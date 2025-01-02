#!/usr/bin/python

import numpy as np


# Diagonal entries required in shape of 'X'
directions  = [[1,1], [-1,-1]]
directions2 = [[-1,1], [1,-1]]

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
    Xlist = []
    for p in where_2d(arr, 'M'):
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
            Xlist.append([p[0]+direction[0], p[1]+direction[1]])
    return Xlist

def create_set(Xlist, stride):
    # Generate a unique hash for each pair
    s = set()
    for e in Xlist:
        h = stride*e[1] + e[0]
        s.add(h)
    return s


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

print("X-search pass 1") 
num_matches = 0
Xlist1 = []
for d in directions:
    Xlist1 = Xlist1 + word_search(y, "MAS", d)

Xlist2 = []
print("X-search pass 2") 
for d in directions2:
    Xlist2 = Xlist2 + word_search(y, "MAS", d)

inter =  create_set(Xlist1, 200)
inter2 = create_set(Xlist2, 200)

num_matches = len(inter.intersection(inter2))
print("Found %d matches" % num_matches)
