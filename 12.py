#! /usr/bin/env python

import os.path
from time import time


class Pattern:
    def __init__(self, in_, out):
        self.in_ = in_
        self.out = out


def fix_array(offset, arr):
    if "#" not in arr:
        return offset, arr

    # Fix start
    s = 0
    for i in range(len(arr)):
        if arr[i] == "#":
            s = i
            break

    if s < 3:
        x = 3 - s
        offset -= x
        arr = ["."] * x + arr
    elif s > 3:
        x = s - 3
        offset += x
        arr = arr[x:]

    # Fix end
    s = 0
    for i in range(len(arr)):
        if arr[-(i + 1)] == "#":
            s = i
            break

    if s < 3:
        x = 3 - s
        arr = arr + ["."] * x
    elif s > 3:
        x = s - 3
        arr = arr[:-x]

    return offset, arr


def sum_plants(arr, offset):
    return sum(i + offset for i, c in enumerate(arr) if c == "#")


def main():
    patterns = []
    generations = 20
    offset = 0

    with open(os.path.join("input", "12.txt")) as f:
        l1 = f.readline()
        og_array = [c for c in l1 if c in (".", "#")]
        _ = f.readline()

        for l in f:
            in_, out = l.split(" => ")
            out = out[0]
            patterns.append(Pattern(in_, out))

    arr = og_array[:]

    for gen in range(generations):
        offset, arr = fix_array(offset, arr)
        arr_new = []
        for i in range(0, len(arr)):
            if i < 2 or i > len(arr) - 2:
                arr_new.append(".")
                continue

            cur = "".join(arr[i - 2 : i + 3])

            for p in patterns:
                if cur == p.in_:
                    arr_new.append(p.out)
                    break
            else:
                arr_new.append(".")

        arr = arr_new

    s = sum_plants(arr, offset)
    print("Part 1: %d" % s)

    arr = og_array[:]
    offset = 0

    prev_cksum = 0
    c = 0
    offset_delta = 0
    prev_offset = 0
    last_gen = 0
    generations = 50000000000
    for gen in range(generations):
        offset, arr = fix_array(offset, arr)
        arr_new = []
        for i in range(0, len(arr)):
            if i < 2 or i > len(arr) - 2:
                arr_new.append(".")
                continue

            cur = "".join(arr[i - 2 : i + 3])

            for p in patterns:
                if cur == p.in_:
                    arr_new.append(p.out)
                    break
            else:
                arr_new.append(".")

        cksum = sum(i if c == "#" else 0 for i, c in enumerate(arr))

        if cksum == prev_cksum and offset - prev_offset == offset_delta:
            c += 1

            if c == 100:
                last_gen = gen + 1
                arr = arr_new
                print("Stopped at gen %d offset is %d" % (last_gen, offset))
                break
        else:
            c = 0

        arr = arr_new
        prev_cksum = cksum
        offset_delta = offset - prev_offset
        prev_offset = offset

    s = sum_plants(arr, offset)
    nb = len([c for c in arr if c == "#"])
    s = (generations - last_gen) * nb + s
    print("Part 2: %d" % s)


if __name__ == "__main__":
    ts = time()
    main()
    ts = time() - ts
    print("Done in %.3fms" % (ts * 1000))
