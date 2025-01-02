#!/usr/bin/python

from part2 import Comp
from part2 import read_program
import sys

f = open("input")
state = read_program(f)
f.close()

# Override regA if provided
if len(sys.argv) == 2:
    regA = int(sys.argv[1])
    state[0][0] = regA
    print(f"Register A override: {regA}")

# The required output
matching = state[1]
#print(matching)

def cycle_states(start, n, shl, thresh):
    found = list()
    for x in range(n):
        # shift is in octal digits
        state[0][0] = (start << (3 * shl)) + (x << 3)
        test = Comp(state[0], state[1])
        test.run()
        count = test.compare(matching)
        # threshold for continuing search
        if count >= thresh:
            print(f"{state[0][0]} = {state[0][0]:#o} matches {count} digits: {test.get_octal()}.")
            mask = (8 << (3 * shl)) - 1
            found.append(state[0][0] & ~mask)
    return(found)

trials = [200000]
#ans = 35184372088832 ## 1 << 45 = o'1 000 000 000 000 000

# Trial solutions
# - The SHR/DIV operation allows up to 2^7 variations (single octal digit)
# - If N is a solution, then N+1...N+6 are all solutions, so the final digit can be ignored

#   1762416 = 0o6562160 matches 6 digits: [0, 4, 3, 5, 5, 3, 0].
#  14099336 = 0o65621610 matches 7 digits: [7, 3, 4, 3, 5, 5, 3, 0].
# 112795008 = 0o656216600 matches 8 digits: [6, 0, 3, 4, 3, 5, 5, 3, 0].

for y in range(12):
    print(f"Search {len(trials)} candidates for {y + 6} matching digits.")
    trials2 = list()
    for t in trials:
        trials2 += cycle_states(t, 1*512*512, 1, y + 6)
        if len(trials2) == 0:
            print("Warning: search failed.")
            sys.exit(1)
    # remove duplicates
    trials = list(set(trials2))

