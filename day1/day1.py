#!/usr/bin/python

# --- Day 1: Historian Hysteria ---

lista = []
listb = []
file = open("input")
for line in file:
    (a, b) = line.split()
    lista.append(int(a))
    listb.append(int(b))
file.close()

print("Sorting lists")
lista.sort()
listb.sort()

print("Calculate distance between items")
total_distance = 0
for x in lista:
    y = listb.pop(0)
    print(y)
    distance = abs(x - y)
    total_distance = total_distance + distance

print("Total distance = %d" % total_distance)
