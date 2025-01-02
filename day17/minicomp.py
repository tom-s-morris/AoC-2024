#!/usr/bin/python

from day17 import Comp
from day17 import read_program
import sys

f = open("input")
state = read_program(f)
f.close()

# Override regA if provided
regA = 2024
if len(sys.argv) == 2:
    regA = int(sys.argv[1])
    state[0][0] = regA
    print(f"Register A override: {regA}")


# Provide short-circuit to control register 'C'
#state[1].pop(4)
#state[1].pop(4)
#my_comp = Comp(state[0], state[1])
#my_comp.disassemble()
#my_comp.run()

# Reverse the hashing algorithm, i.e. B is now input, A is output
# XOR is reversible

# 4,3 : rB = bxc, none
# 1,6 : rB = bxl, #6
# 5,5 : sp = out, rB
prog2 = [4, 3, 1, 6, 5, 5]

A_table_LUT = list()
for regB in range(8):
    row = list()
    for regC in range(8):
        regs = [0, regB, regC]
        comp2 = Comp(regs, prog2)
        #if regC == 0:
        #    comp2.disassemble()
        comp2.run()
        row.append(int(comp2._outputs[0]))
    A_table_LUT.append(row)

print(f"A_table_LUT: {A_table_LUT}")

# A_table_LUT gives the input A-value for the desired output B-value, depending
# on the regC control, which itself depends on the digit in the A sequence.

# Sequence of 'C' values for input 'A'
# 2,4 : rB = bst, rA
# 1,3 : rB = bxl, #3
# 7,5 : rC = cdv, rB
# 0,3 : rA = adv, #3
# 5,6 : sp = out, rC
# 3,0 : sp = jnz, #0
prog3 = [2, 4, 1, 3, 7, 5, 0, 3, 5, 6, 3, 0]

#comp3 = Comp([regA, 0, 0], prog3)
#comp3.disassemble()
#comp3.run()
#regC_seq = comp3.get_octal()

#print(f"RegC sequence: {regC_seq}")


# Method
# For each output B-value, search for compatible values of regC:
#   for B in B_list:
#       for C in range(8):
#           if regC_seq at A_table_LUT[B, C] == C:
#               potential candidate: B would yield A, or A would yield B at step N

# See 'input' file in day17.py
test_output = [6,2,7,2,3,1,6,0,5]

regA = 0
for b in reversed(test_output):
    for c in range(8):
        a = A_table_LUT[b][c]
        # running solution for regA
        comp4 = Comp([regA + 8 * a, 0, 0], prog3) # run program for trial A
        comp4.run()
        regC_seq = list(map(int, comp4._outputs))
        if regC_seq[-1] == c:
            regA = regA * 8 + a
            out = ",".join(comp4._outputs)
            print(f"Match for {regA} = {regA:#o}, yielded comp4.out = {out}")
            # continue, check for other solutions
            break

print(f"Final regA = {regA}")



