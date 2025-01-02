#!/usr/bin/python

# --- Day 19: Linen Layout (Part 2) ---

import re
import sys


# Towel design dictionary: first letter->[pattern A, pattern B]
# Order list by pattern length, to match longest pattern first
# E.g. brwrr => 'bwu' no good, match 'br' to leave 'wrr', otherwise 'b'
colour_LU = dict()

matches = 0

def search(pattern):
    global matches
    p = pattern[:1]
    if p not in colour_LU.keys():
        return
    for s in colour_LU[p]:
        if pattern.startswith(s):
            # continue search
            if pattern == s:
                matches += 1
                continue # check remaining colours
            l = len(s)
            if l >= len(pattern):
                continue
            search(pattern[l:])
    # no towels fit into pattern
    return

def sort_len(e):
    return len(e)

def group_by_first_letter(towels):
    for t in towels:
        key = t[:1]
        if key in colour_LU.keys():
            colour_LU[key].append(t)
        else:
            colour_LU[key] = [t]
    for v in colour_LU.values():
        v.sort(reverse=True, key=sort_len)


# Load linen patterns
def read_data(f):
    designs = list()
    for line in f:
        line = line.rstrip()
        if len(line) == 0:
            continue
        if line.find(",") != -1:
            towels = line.split(", ")
            continue
        m = re.match("([wubrg]+)", line)
        if m:
            designs.append(m.group(1))
    return(designs, towels)


################
# Main program #
################
f = open("input")
data = read_data(f)
f.close()

towels = data[1]

count_sols = 0
group_by_first_letter(towels)
for pattern in data[0]:
    print(f"Checking pattern: {pattern}")
    res = search(pattern)
    if res:
        print(pattern, res)
        count_sols += 1

print(f"Found {count_sols} possible towel designs with {matches} different ways.")

