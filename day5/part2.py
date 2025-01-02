#!/usr/bin/python

import re
import sys
import copy

#sys.setrecursionlimit(2000)

class Page:
    def __init__(self, num):
        self._number = num
        # Example: 47|53 means page(53) is in page(47)._order_after
        self._order_after = []

    def __repr__(self):
        return f"Page '{self._number}'"

    def add_after(self, page):
        self._order_after.append(page)

    def find(self, p2):
        # Check graph as the ordering may already be enforced
        if p2 in self._order_after:
            return True
        else:
            for p in self._order_after:
                if p.find(p2):
                    return True
        return False

def find_or_create_page(num):
    if num in page_dict.keys():
        p = page_dict[num]
    else:
        #print("Create new page %d" % num)
        p = Page(num)
        page_dict[num] = p
    return p

def create_tree(rule):
    num1 = rule[0]
    num2 = rule[1]
    p1 = find_or_create_page(num1)
    p2 = find_or_create_page(num2)
    try:
        if p2.find(p1):
            print("Cyclic dependency! %s <-> %s" % (p1, p2))
            return
        if not p1.find(p2):
            p1.add_after(p2)
    except RecursionError:
        print("Recursion error, dumping state!")
        print("Pair (%d,%d)" % (num1,num2))
        print(page_dict)

def delete_tree(dict):
    for page in dict.values():
        page._order_after.clear()
    dict.clear()

def check_and_fix_update(update):
    status = True
    for idx in range(len(update)):
        if idx == 0:
            continue
        n1 = update[idx-1]
        n2 = update[idx]
        if page_dict[n2].find(page_dict[n1]):
            #print("Error: page %d found before %d. Fixed." % (n1, n2))
            status = False
            update[idx-1] = n2
            update[idx] = n1
    return status

print("Read the printer instructions")
file = open("input")
rules = []
for line in file:
    line2 = line.rstrip()
    if len(line2) == 0:
        # End of page order rules
        break
    m = re.search("(\d+)\|(\d+)", line2)
    n1 = int(m.group(1))
    n2 = int(m.group(2))
    rules.append([n1, n2])

print("Read the updates section")
checksum = 0
page_dict = {}
for line in file:
    update_str = line.rstrip()
    if len(update_str) == 0:
        continue
    update_str2 = update_str.split(",")
    it = map(int, update_str2)
    update = list(it)

    # Add rule to page ordering tree
    rules2 = []
    for r in rules:
        if r[0] in update and r[1] in update:
            rules2.append(r)

    delete_tree(page_dict)
    for r in rules2:
        create_tree(r)
    if not check_and_fix_update(update):
        while True:
            # re-check the order
            if check_and_fix_update(update):
                break
        print(update)
        mid = (len(update) - 1)//2
        checksum = checksum + int(update[mid])
file.close()

print(checksum)
