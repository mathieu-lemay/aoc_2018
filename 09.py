#! /usr/bin/env python

from time import time
import psutil

_id = 0


class Marble:
    __slots__ = ('val', 'prev', 'next')

    def __init__(self, val, prev=None, next_=None):
        self.val = val
        self.prev = prev or self
        self.next = next_ or self


def get_high_score(nb_players, last_marble):
    marble = Marble(0, None, None)
    scores = {}

    p = 0

    for v in range(1, last_marble+1):
        if v % 1000000 == 0:
            print('%8d | %5.1f%%' % (v, v / last_marble * 100))

        if v % 23 == 0:
            for _ in range(7):
                marble = marble.prev

            scores[p] = scores.get(p, 0) + v + marble.val

            prev = marble.prev
            next_ = marble.next

            prev.next = next_
            next_.prev = prev
            marble = next_
        else:
            marble = marble.next.next
            prev = marble.prev

            new_m = Marble(v, prev, marble)

            prev.next = new_m
            marble.prev = new_m

            marble = new_m

        p += 1

        if p == nb_players:
            p = 0

    print('Memory: %s' % get_human_readable_size(psutil.Process().memory_info().rss))

    return max(scores.values())


def get_human_readable_size(size):
    for unit in ('B', 'KiB', 'MiB', 'GiB', 'TiB'):
        if size < 1024:
            return '%.2f %s' % (size, unit)
        elif unit == 'TiB':
            return '%d %s' % (round(size), unit)

        size /= 1024


def main():
    print("Part 1: %d" % get_high_score(458, 72019))
    print("Part 2: %d" % get_high_score(458, 7201900))


if __name__ == '__main__':
    ts = time()
    main()
    ts = time() - ts
    print('Done in %.3fms' % (ts * 1000))
