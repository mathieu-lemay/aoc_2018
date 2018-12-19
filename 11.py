#! /usr/bin/env python

from time import time

import numpy as np


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
    grid_serial = 7989
    grid_size = 300

    grid = np.zeros((grid_size, grid_size))

    for i in range(grid_size):
        for j in range(grid_size):
            x = i + 1
            y = j + 1
            rack_id = x + 10
            grid[i, j] = (((((rack_id * y) + grid_serial) * rack_id) // 100) % 10) - 5

    x1 = y1 = v1 = 0
    for i in range(grid_size - 3):
        x = i + 1
        for j in range(grid_size - 3):
            y = j + 1
            s = np.sum(grid[i:i+3, j:j+3])
            if s > v1:
                x1 = x
                y1 = y
                v1 = s

    print('Part 1: %d,%d' % (x1, y1))

    x2 = y2 = k2 = v2 = 0
    for i in range(grid_size - 3):
        x = i + 1
        print('P2: x = %d' % x)
        for j in range(grid_size - 3):
            y = j + 1
            for k in range(grid_size - max(i, j)):
                s = np.sum(grid[i:i+k, j:j+k])
                if s > v2:
                    x2 = x
                    y2 = y
                    k2 = k
                    v2 = s

    print('Part 2: %d,%d,%d' % (x2, y2, k2))


if __name__ == '__main__':
    ts = time()
    main()
    ts = time() - ts
    print('Done in %.3fms' % (ts * 1000))
