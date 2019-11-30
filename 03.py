#! /usr/bin/env python

import os.path
import re

import numpy as np


class Claim:
    def __init__(self, id_, x, y, w, h):
        self.id = int(id_)
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        self.x2 = self.x + self.w
        self.y2 = self.y + self.h

    def __repr__(self):
        return "<Claim(id=%d, x=%d, y=%d, w=%d, h=%d)>" % (
            self.id,
            self.x,
            self.y,
            self.w,
            self.h,
        )

    def __and__(self, o):
        max_x = max((self.x, o.x))
        min_w = min((self.x2, o.x2))

        max_y = max((self.y, o.y))
        min_h = min((self.y2, o.y2))

        return max_x <= min_w and max_y <= min_h


def main():
    claims = []

    with open(os.path.join("input", "03.txt")) as f:
        matcher = re.compile(r"#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)")
        for l in f:
            m = matcher.match(l)
            id_ = m.group(1)
            x = m.group(2)
            y = m.group(3)
            w = m.group(4)
            h = m.group(5)

            claims.append(Claim(id_, x, y, w, h))

    area_w = max(c.x + c.w for c in claims)
    area_h = max(c.y + c.h for c in claims)

    print(area_w, area_h)

    arr = np.zeros((area_w, area_h))

    for c in claims:
        c_arr = np.zeros((area_w, area_h))
        c_arr[c.x : c.x + c.w, c.y : c.y + c.h] = 1

        arr += c_arr

    c = np.where(arr > 1)
    print("Part 1 -> %d" % c[0].size)

    for i, c1 in enumerate(claims):
        has_overlap = False
        for j, c2 in enumerate(claims):
            if i == j:
                continue

            if c1 & c2:
                has_overlap = True
                break

        if not has_overlap:
            print("Part 2 -> %s" % c1)
            break


if __name__ == "__main__":
    main()
