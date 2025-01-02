#!/usr/bin/python

# --- Day 17: Chronospatial Computer ---

import re
import sys

# 3-bit computer with 8 instructions and 3 (integer, arbitrary length) registers A, B, and C.
# Each operand is also 3-bits in size. Operand can be literal or combo (register).
#  l0 to l7 are literal values d'0 to d'7
#  c0 to c3 are literal values d'0 to d'3
#  c4 to c6 source the operand from registers A, B and C respectively
#  c7 is reserved

# Instruction set
#  0 - adv (division, result in rA)
#  1 - bxl (bitwise: rB XOR imm)
#  2 - bst (bitmask with b'111)
#  3 - jnz (jump if not zero)
#  4 - bxc (bitwise: rB XOR rC). Operand is ignored
#  5 - out (display operand modulo 8)
#  6 - bdv (division, result in rB)
#  7 - cdv (division, result in rC)

mnemonics =  ["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv"]
# Source can be immediate/literal or combo
literal_op = [False, True,  False, True,  False, False, False, False]
combo_op =   [True,  False, True,  False, False, True,  True,  True]

# register dest, 0 = N/A
dest_reg = [4, 5, 5, 0, 5, 0, 5, 6]

registers = ("rA", "rB", "rC")
def reg(c):
    return registers[c-4]

# 3-bit lookup table
not_LUT = [7, 6, 5, 4, 3, 2, 1, 0]


#
# Computer representation
#
class Comp:
    def __init__(self, regs, program):
        if len(regs) != 3:
            raise RuntimeError("Three register values expected.")
        if len(program) % 2 == 1:
            raise RuntimeError("Program mismatch. Missing operand after last instruction?")
        self._r = list(regs)
        self._prog_code = program[::2]
        self._prog_operands = program[1::2]
        self._pc = 0 # program counter/instruction pointer
        self._outputs = []
        self._octal = []
        self.validate()
        self._debug = False

    def validate(self):
        if min(self._prog_code) < 0 or max(self._prog_code) > 7:
            raise RuntimeError("Invalid instruction code")

    def disassemble(self):
        for c, code in enumerate(self._prog_code):
            operand = self._prog_operands[c]
            if literal_op[code]:
                src = "#" + str(operand)
            elif combo_op[code]:
                if operand < 4:
                    src = "#" + str(operand)
                elif operand < 7:
                    src = reg(operand)
                else:
                    src = "reserved"
            else:
                src = "none" # ignored by bxc

            rd = dest_reg[code]
            dest = reg(dest_reg[code]) if rd > 0 else "sp"
            print(f"{code},{operand} : {dest} = {mnemonics[code]}, {src}")
        print("Stop.")

    def run(self):
        # Fetch the next opcode and operand
        while self._pc < len(self._prog_code):
            c = self._pc
            code = self._prog_code[c]
            operand = self._prog_operands[c]
            self._pc = self.pipeline(code, operand)
        #self.print()

    def print_regs_octal(self):
        print(f"A= {self._r[0]:#o}  B= {self._r[1]:#o}  C= {self._r[2]:#o}")

    def pipeline(self, opc, operand):
        # Decode and execute the current instruction
        if opc == 0:
            src2 = self.reg_or_immediate(operand)
            self.division(self._r[0], src2, 0) # dest = rA
        elif opc == 1:
            self.bitwise_XOR(operand)
        elif opc == 2:
            src = self.reg_or_immediate(operand)
            self.mask_low3(src)
        elif opc == 3:
            if self._r[0] > 0:
                if self._debug:
                    self.print_regs_octal()  # log register state
                return operand  # new PC
        elif opc == 4:
            # BXC takes no operands
            self.bitwise_XOR_reg()
        elif opc == 5:
            src = self.reg_or_immediate(operand)
            self.output(src)
        elif opc == 6:
            src2 = self.reg_or_immediate(operand)
            self.division(self._r[0], src2, 1) # dest = rB
        elif opc == 7:
            src2 = self.reg_or_immediate(operand)
            self.division(self._r[0], src2, 2) # dest = rC
        return self._pc + 1

    # return combo source
    def reg_or_immediate(self, n):
        if n < 4:
            return n
        elif n < 7:
            return self._r[n - 4]
        else:
            raise RuntimeError(f"Unknown combo source {n}")

    def division(self, src1, src2, dest):
        x = src1
        y = 2 ** src2
        self._r[dest] = x // y

    # BXL, dest = rB
    def bitwise_XOR(self, src):
        # do XOR, use 3-bit lookup table
        #not_src = not_LUT[src]
        i0 = self._r[1] & (~ src)
        i1 = (~ self._r[1]) & src
        self._r[1] = i0 | i1

    # BST, dest = rB
    def mask_low3(self, src):
        self._r[1] = src % 8

    # BXC, dest = rB
    def bitwise_XOR_reg(self):
        i0 = self._r[1] & (~ self._r[2])
        i1 = (~ self._r[1]) & self._r[2]
        self._r[1] = i0 | i1

    def output(self, src):
        self._octal.append(src % 8)
        self._outputs.append(str(src % 8))
        #print(f"Src = {src % 8}")

    def get_octal(self):
        return self._octal

    def compare(self, matching):
        for idx, m in enumerate(reversed(self._octal)):
            if m != matching[-1-idx]:
                break
        return idx

    def print(self):
        print(",".join(self._outputs))

# Load program and register inputs
def read_program(f):
    regs = [0, 0, 0]
    for line in f:
        line = line.rstrip()
        if len(line) == 0:
            continue
        m = re.match("Register ([ABC]{1}): (\d+)", line)
        if m:
            if m.group(1) == "A":
                regs[0] = int(m.group(2))
            elif m.group(1) == "B":
                regs[1] = int(m.group(2))
            elif m.group(1) == "C":
                regs[2] = int(m.group(2))
            else:
                raise RuntimeError(f"Unknown register {m.group(1)}")
        else:
            m = re.match("Program: ([\d,]+)", line)
            program = list(map(int, m.group(1).split(",")))
    return (regs, program)

f = open("input")
state = read_program(f)
f.close()

# Override regA if provided
if len(sys.argv) == 2:
    regA = int(sys.argv[1])
    state[0][0] = regA
    print(f"Register A override: {regA}")

my_comp = Comp(state[0], state[1])
my_comp.disassemble()
my_comp._debug = True
my_comp.run()
my_comp.print()

# The required output
matching = state[1]
#print(matching)

def cycle_states(start, n, shl, thresh):
    found = list()
    for x in range(n):
        # shift is in octal digits
        state[0][0] = start + (x << (3 * shl))
        test = Comp(state[0], state[1])
        test.run()
        count = test.compare(matching)
        # threshold for continuing search
        if count >= thresh:
            print(f"{state[0][0]} = {state[0][0]:#o} matches {count} digits: {test.get_octal()}.")
            mask = (8 << (3 * shl)) - 1
            found.append(state[0][0] & ~mask)
    return(found)

trials = [0]
#ans = 35184372088832 ## 1 << 45 = o'1 000 000 000 000 000

# Trial solutions
# - The SHR/DIV operation allows up to 2^7 variations (single octal digit)
# - If N is a solution, then N+1...N+6 are all solutions, so the final digit can be ignored

#for y in range(4):
#    for t in trials:
#        print(f"Search {len(trials)} candidates for {y + 6} matching digits.")
#        trials = cycle_states(t, 4*512*512, y + 1, y + 6)
#        if len(trials) == 0:
#            print("Warning: search failed.")
#            sys.exit(1)

