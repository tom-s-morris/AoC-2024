#!/usr/bin/python

import sys
import re
import math

def offset(x):
    return x + 10000000000000
def parse_file(f):
    problem_list = []
    for line in f:
        line = line.rstrip()
        if len(line) == 0:
            continue
        m = re.match("Button ([AB]{1}): X\+(\d+), Y\+(\d+)", line)
        if m:
            if m.group(1) == "A":
                xA = int(m.group(2))
                yA = int(m.group(3))
            elif m.group(1) == "B":
                xB = int(m.group(2))
                yB = int(m.group(3))
            else:
                raise RuntimeError(f"Unknown button {m.group(1)}")
        else:
            m = re.match("Prize: X=(\d+), Y=(\d+)", line)
            xC = int(m.group(1))
            yC = int(m.group(2))
            # Part Two: offset the prize location
            xC = offset(xC)
            yC = offset(yC)
            problem_list.append([xA, xB, xC, yA, yB, yC])
    return problem_list

# determinant of the 2x2 matrix
def determinant(mat):
    det = mat[0]*mat[4] - mat[1]*mat[3]
    if det != 0:
        print("Unique solution")
    return det

def solve(mat):
    d = determinant(mat)
    if d != 0:
        # remove factor 1/d which causes loss of precision
        inv = [mat[4], -1 * mat[1], -1 * mat[3], mat[0]]
        nA = inv[0] * mat[2] + inv[1] * mat[5]
        nB = inv[2] * mat[2] + inv[3] * mat[5]
        # Only integer solution is valid
        if nA % d == 0 and nB % d == 0:
            nA = nA / d
            nB = nB / d
            print(f"Solution: {nA} and {nB}")
            tokens = 3 * nA + nB
            return tokens
    return 0

f = open("input")
problems = parse_file(f)
f.close()

tokens = 0
for coeffs in problems:
    t = solve(coeffs)
    tokens += t

print("Tokens used: %d" % tokens)

