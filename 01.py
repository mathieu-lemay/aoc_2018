#! /usr/bin/env python

import os.path

freq = 0
freqs = {freq}

dupe_found = False

with open(os.path.join("input", "01.txt")) as f:
    inputs = [int(l) for l in f]

print("Result: %d" % sum(inputs))

freq = 0
while not dupe_found:
    for d in inputs:
        freq += d

        if freq in freqs:
            print("First dupe: %d" % freq)
            dupe_found = True
            break

        freqs.add(freq)
