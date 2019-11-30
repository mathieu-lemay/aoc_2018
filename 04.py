#! /usr/bin/env python

import os.path
import re
from datetime import datetime

import numpy as np


class Guard:
    def __init__(self, id_):
        self.id = id_
        self.pattern = np.zeros((60,))
        self.minutes_sleep = 0

    def __repr__(self):
        return "<Guard(id=%d, minutes_sleep=%d)>" % (self.id, self.minutes_sleep)


def main():
    guards = {}

    guard = None

    with open(os.path.join("input", "04.txt")) as f:
        ts_pattern = r"\[([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2})\] "
        shift_matcher = re.compile(ts_pattern + r"Guard #([0-9]+) begins shift")
        sleep_matcher = re.compile(ts_pattern + r"falls asleep")
        wakes_matcher = re.compile(ts_pattern + r"wakes up")

        sleep_start = None

        for line in f:
            line = line[:-1]
            m = shift_matcher.match(line)
            if m:
                id_ = int(m.group(2))
                guard = guards.get(id_)
                if not guard:
                    guard = Guard(id_)
                    guards[id_] = guard

                continue

            m = sleep_matcher.match(line)
            if m:
                ts = m.group(1)
                if sleep_start:
                    raise ValueError("Guard is already sleeping: %s" % ts)

                sleep_start = datetime.strptime(ts, "%Y-%m-%d %H:%M")
                continue

            m = wakes_matcher.match(line)
            if m:
                ts = m.group(1)
                if not sleep_start:
                    raise ValueError("Guard is not sleeping: %s" % ts)

                sleep_end = datetime.strptime(ts, "%Y-%m-%d %H:%M")

                start_minute = sleep_start.minute
                end_minute = sleep_end.minute

                arr = np.zeros((60,))
                arr[start_minute:end_minute] = 1

                guard.pattern += arr
                sleep_start = None

                continue

    for k, v in guards.items():
        minutes = np.sum(v.pattern)
        v.minutes_sleep = minutes

        if minutes > guard.minutes_sleep:
            guard = v

    pattern = guard.pattern
    minute_most_slept = pattern.argsort()[-1]

    print("Part 1 -> %d" % (minute_most_slept * guard.id))

    count = minute = 0
    for k, v in guards.items():
        m = v.pattern.argsort()[-1]
        c = v.pattern[m]

        if c > count:
            guard = v
            count = c
            minute = m

    print(guard.pattern)
    print("Part 2 -> %d" % (guard.id * minute))


if __name__ == "__main__":
    main()
