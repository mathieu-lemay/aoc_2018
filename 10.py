#! /usr/bin/env python

import os.path
import re
from time import time


class Point:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self, n):
        self.x = self.x + self.vx * n
        self.y = self.y + self.vy * n

    def distance(self, o):
        return abs(self.x - o.x) + abs(self.y - o.y)

    def __repr__(self):
        cname = self.__class__.__name__
        attrs = ', '.join('%s=%s' % (k, v) for k, v in self.__dict__.items())
        return '<%s(%s)>' % (cname, attrs)


def main():
    points = []

    with open(os.path.join('input', '10.txt')) as f:
        pattern = r'position=<([- ][0-9]+), ([- ][0-9]+)> velocity=<([- ][0-9]+), ([- ][0-9]+)>'
        matcher = re.compile(pattern)

        for l in f:
            m = matcher.match(l[:-1])
            x = int(m.group(1))
            y = int(m.group(2))
            vx = int(m.group(3))
            vy = int(m.group(4))

            points.append(Point(x, y, vx, vy))

    total_steps = 0

    _, _, w, h = get_grid_coords(points)
    print('Grid size: %dx%d' % (w, h))
    while True:
        # steps = 10612
        steps = int(input("How many steps? "))
        if steps == 0:
            break

        total_steps += steps
        print('Steps taken: %d' % total_steps)

        for p in points:
            p.move(steps)

        _, _, w, h = get_grid_coords(points)
        print('Grid size: %dx%d' % (w, h))
        i = input("Print? ")
        if i.lower() == 'y':
            print_points(points)


def get_grid_coords(points):
    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)
    return min_x, min_y, max_x - min_x + 1,  max_y - min_y + 1


def print_points(points):
    x, y, w, h = get_grid_coords(points)

    grid = [[' '] * w for _ in range(h)]

    for p in points:
        grid[p.y - y][p.x - x] = '#'

    for r in grid:
        print(''.join(r))


if __name__ == '__main__':
    ts = time()
    main()
    ts = time() - ts
    print('Done in %.3fms' % (ts * 1000))
