#!/usr/bin/python

# --- Day 3: Mull It Over ---

import re

def find_numbers(text):
    x = re.findall("mul\(\d+,\d+\)", text)
    sum = 0
    for s in x:
        print(s)
        m = re.match("mul\((\d+),(\d+)\)", s)
        a = int(m.group(1))
        b = int(m.group(2))
        sum = sum + a*b
    print("Sum of valid instructions = %d" % sum)

file = open("input", 'r')
file_content = file.read()
find_numbers(file_content)
file.close()

