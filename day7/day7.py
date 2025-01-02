#!/usr/bin/python

# --- Day 7: Bridge Repair ---

import sys
from itertools import product


def calculate(num_list, p):
    x = num_list[0]
    idx = 0
    for op in list(p):
        idx = idx + 1
        y = num_list[idx]
        if op == 1:
            x = x + y
        else:
            x = x * y
    return x

def test(target, num_list):
    for p in product(range(2), repeat=len(num_list) - 1):
        ans = calculate(num_list, p)
        if ans ==  target:
            return True
    return False

tot = 0
with open("input", "r") as f:
    for line in  f:
        line2 = line.rstrip()
        if len(line2) == 0:
            continue
        (n, string) = line2.split(':')
        target = int(n)
        string2 = string.lstrip()
        num_list = string2.split(' ')
        num_list2 = list(map(int, num_list))
        if test(target, num_list2):
            tot += target
            print(target)

print(f"Total '{tot}'")
