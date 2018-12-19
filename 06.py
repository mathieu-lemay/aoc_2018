#! /usr/bin/env python

import os.path

import numpy as np


class Point:
    def __init__(self, id_, x, y):
        self.id = id_
        self.x = x
        self.y = y
        self.is_edge = False

    def __repr__(self):
        cname = self.__class__.__name__
        attrs = ', '.join('%s=%s' % (k, v) for k, v in self.__dict__.items())
        return '<%s(%s)>' % (cname, attrs)

    def distance(self, o):
        return abs(self.x - o.x) + abs(self.y - o.y)


def main():
    coordinates = []

    with open(os.path.join('input', '06.txt')) as f:
        for idx, l in enumerate(f):
            x, y = [int(i.strip()) for i in l.split(',')]
            coordinates.append(Point(idx + 1, x, y))

    min_x = min(c.x for c in coordinates) - 10
    max_x = max(c.x for c in coordinates) + 10
    min_y = min(c.y for c in coordinates) - 10
    max_y = max(c.y for c in coordinates) + 10
    w = max_x - min_x + 1
    h = max_y - min_y + 1

    arr = np.zeros((w, h))

    for x in range(w):
        for y in range(h):
            p = Point(None, x + min_x, y + min_y)
            closest_distance = w * h
            closest_points = []
            for c in coordinates:
                d = p.distance(c)
                if d < closest_distance:
                    closest_points = [c]
                    closest_distance = d
                elif d == closest_distance:
                    closest_points.append(c)

            if len(closest_points) == 1:
                arr[x, y] = closest_points[0].id

    edge_ids = set(arr[0, :]) | set(arr[w-1, :]) | set(arr[:, 0]) | set(arr[:, h-1])

    counts = sorted([(id_, c) for id_, c in zip(*np.unique(arr, return_counts=True)) if id_ not in edge_ids],
                    key=lambda x: x[1], reverse=True)
    print('Part 1 ->', counts[0][1])

    min_x = min(c.x for c in coordinates)
    max_x = max(c.x for c in coordinates)
    min_y = min(c.y for c in coordinates)
    max_y = max(c.y for c in coordinates)
    w = max_x - min_x + 1
    h = max_y - min_y + 1

    arr = np.zeros((w, h))

    for x in range(w):
        for y in range(h):
            p = Point(None, x + min_x, y + min_y)
            total_distance = sum(p.distance(c) for c in coordinates)

            if total_distance < 10000:
                arr[x, y] = 1

    counts = sorted([(id_, c) for id_, c in zip(*np.unique(arr, return_counts=True))],
                    key=lambda x: x[1], reverse=True)
    print('Part 2 ->', int(arr.sum()))


if __name__ == '__main__':
    main()
