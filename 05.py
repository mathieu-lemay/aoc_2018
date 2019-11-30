#! /usr/bin/env python

import os.path
import string


def main():
    og_data = []
    with open(os.path.join("input", "05.txt")) as f:
        buffer = f.read(2048)
        while buffer:
            og_data += list(buffer)
            buffer = f.read(2048)

    if og_data[-1] == "\n":
        og_data.pop(len(og_data) - 1)

    data = og_data[:]

    data_len = len(data)
    i = 0
    while i < data_len - 1:
        a = data[i]
        b = data[i + 1]
        if a != b and a.lower() == b.lower():
            data.pop(i)
            data.pop(i)
            data_len = len(data)
            if i > 0:
                i -= 1
        else:
            i += 1

    print("Part 1 -> %d" % len(data))

    sizes = []

    for p in string.ascii_lowercase:
        data = [x for x in og_data if x.lower() != p]

        data_len = len(data)
        i = 0
        while i < data_len - 1:
            a = data[i]
            b = data[i + 1]
            if a != b and a.lower() == b.lower():
                data.pop(i)
                data.pop(i)
                data_len = len(data)
                if i > 0:
                    i -= 1
            else:
                i += 1

        sizes.append((p, len(data)))

    sizes.sort(key=lambda x: x[1], reverse=True)

    print("Part 2 -> %d" % (sizes[-1][1]))


if __name__ == "__main__":
    main()
