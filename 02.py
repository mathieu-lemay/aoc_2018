#! /usr/bin/env python

from itertools import groupby

import os.path


class FoundIt(Exception):
    pass


sr_with_d = []
sr_with_t = []

with open(os.path.join('input', '02.txt')) as f:
    inputs = f.readlines()

for sr in inputs:
    sizes = {len(list(v)) for _, v in groupby(sorted(list(sr[:-1])))}

    if 2 in sizes:
        sr_with_d.append(sr)

    if 3 in sizes:
        sr_with_t.append(sr)

count_d = len(sr_with_d)
count_t = len(sr_with_t)

print('Part 1 -> D: %d, T: %d, C: %d' % (count_d, count_t, count_d * count_t))

srs = list(set(sr_with_d + sr_with_t))

try:
    for s1 in srs[:-1]:
        for s2 in srs[1:]:
            nb_d = 0
            s3 = ''
            for i, j in zip(s1, s2):
                if i == j:
                    s3 += i
                else:
                    nb_d += 1

            if nb_d == 1:
                raise FoundIt(s3)
except FoundIt as e:
    print("Part 2 -> %s" % e)
else:
    print("Not Found!")
