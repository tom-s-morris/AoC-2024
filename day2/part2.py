#!/usr/bin/python

import copy

def check_report_is_safe(report):
    if len(report) == 0:
        # Empty report/blank line
        return False
    if report[1] == report[0]:
        return False
    increasing = True if report[1] > report[0] else False
    for x in range(len(report) - 1):
        # Must be all increasing or all decreasing
        if increasing:
            if report[x+1] <= report[x]:
                return False
        else:
            if report[x+1] >= report[x]:
                return False
        # Differ by at least 1 (already confirmed) and at most 3
        if abs(report[x+1] - report[x]) > 3:
            return False
    return True

def problem_dampener_is_safe(report):
    # Try removing a single bad level
    for x in range(len(report)):
        report3 = copy.deepcopy(report)
        report3.pop(x)
        if check_report_is_safe(report3):
            return True
    return False

print("Counting safe lists")
file = open("input")
safe_count = 0
for line in file:
    report = line.split()
    report2 = []
    for x in report:
        report2.append(int(x))
    if check_report_is_safe(report2):
        #print(report2)
        safe_count = safe_count + 1
    elif problem_dampener_is_safe(report2):
        print(report2)
        safe_count = safe_count + 1
file.close()

print("Total number of safe lists = %d" % safe_count)
