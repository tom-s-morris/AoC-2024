#!/usr/bin/python

# --- Day 13: Claw Contraption ---

import sys
import re
import math

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
            problem_list.append([xA, xB, xC, yA, yB, yC])
    return problem_list

# determinant of the 2x2 matrix
def determinant(mat):
    det = mat[0]*mat[4] - mat[1]*mat[3]
    if det != 0:
        print("Unique solution")
    return det

def check_integer(x):
    if abs(x - round(x)) < 1E-10:
        return True
    else:
        return False

def solve(mat):
    d = determinant(mat)
    if d != 0:
        inv = [1/d * mat[4], -1/d * mat[1], -1/d * mat[3], 1/d*mat[0]]
        nA = inv[0] * mat[2] + inv[1] * mat[5]
        nB = inv[2] * mat[2] + inv[3] * mat[5]
        print(f"Solution: {nA} and {nB}")
        if check_integer(nA) and check_integer(nB):
            tokens = 3 * round(nA) + round(nB)
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

