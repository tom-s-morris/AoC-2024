#!/usr/bin/python

import sys
from itertools import product
import copy

def calculate(num_list, p):
    x = num_list[0]
    idx = 0
    for op in p:
        idx = idx + 1
        y = num_list[idx]
        if op == 2:
            x = int(str(x)+str(y))
        elif op == 1:
            x = x + y
        else:
            x = x * y
    return x


#' 3563922390719' too low, allow multiple concatenation ops?
def test(target, num_list):
    for p in product(range(3), repeat=len(num_list) - 1):
        ans = calculate(num_list, list(p))
        if ans ==  target:
            return True
    return False

#print(test(7290, [6, 8, 6, 15]))
#sys.exit(0)

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
