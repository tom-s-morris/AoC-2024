#!/usr/bin/python

import re

enable_list = []
disable_list = []

def is_enabled(position):
    xs = 0
    # Find the most recent control word before position
    for x in enable_list:
        if x > position:
            break
        xs = x
    ys = -1
    for y in disable_list:
        if y > position:
            break
        ys = y
    #print(xs, ys)
    if xs > ys:
        return True
    else:
        return False

def find_numbers(text):
    xi = re.finditer("mul\((\d+),(\d+)\)", text)
    sum = 0
    for m in xi:
        if is_enabled(m.start()):
            a = int(m.group(1))
            b = int(m.group(2))
            print(a,b)
            sum = sum + a*b
    print("Sum of valid instructions = %d" % sum)

def find_control_words(text):
    xi = re.finditer("do\(\)", text)
    for m in xi:
        enable_list.append(m.start())
    yi = re.finditer("don't\(\)", text)
    for m in yi:
        disable_list.append(m.start())


file = open("input", 'r')
file_content = file.read()

find_control_words(file_content)
find_numbers(file_content)

file.close()

