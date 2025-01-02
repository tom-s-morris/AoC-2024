#!/usr/bin/python

lista = []
listb = []
file = open("input")
for line in file:
    (a, b) = line.split()
    lista.append(int(a))
    listb.append(int(b))
file.close()

print("Calculate similarity between items")
similarity = 0
for x in lista:
    # Note this is slow as it traverses the whole list, but for 1000 items it's OK.
    y = listb.count(x)
    print(y)
    similarity = similarity + x*y

print("Similarity = %d" % similarity)
