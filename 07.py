#! /usr/bin/env python

import os.path
import re


class Step:
    def __init__(self, id_):
        self.id = id_
        self.nexts = []
        self.prevs = []

    def __repr__(self):
        cname = self.__class__.__name__
        # attrs = ', '.join('%s=%s' % (k, v) for k, v in self.__dict__.items())
        # return '<%s(%s)>' % (cname, attrs)

        prevs = ", ".join(s.id for s in self.prevs)
        nexts = ", ".join(s.id for s in self.nexts)
        return "<%s(id=%s, prevs=[%s], nexts=[%s])>" % (cname, self.id, prevs, nexts)


class Worker:
    def __init__(self, id_):
        self.id = id_
        self.step = None
        self.remaining = None


def main():
    steps = {}

    with open(os.path.join("input", "07.txt")) as f:
        matcher = re.compile(
            r"Step ([A-Z]) must be finished before step ([A-Z]) can begin."
        )

        for l in f:
            m = matcher.match(l)
            if not m:
                raise ValueError(l)

            a = m.group(1)
            b = m.group(2)

            sa = steps.get(a)
            if not sa:
                sa = Step(a)
                steps[a] = sa

            sb = steps.get(b)
            if not sb:
                sb = Step(b)
                steps[b] = sb

            sa.nexts.append(sb)
            sb.prevs.append(sa)

    queue = [s for s in steps.values() if not s.prevs]
    done = []

    while queue:
        n = next(
            s
            for s in sorted(queue, key=lambda x: x.id)
            if all(i.id in done for i in s.prevs)
        )
        queue.remove(n)

        done.append(n.id)
        queue += [s for s in n.nexts if s not in queue]

    print("Part 1 -> %s" % "".join(done))

    queue = [s for s in steps.values() if not s.prevs]
    done = []
    time = -1
    workers = [Worker(i) for i in range(5)]

    while queue or any(w.step for w in workers):
        time += 1

        for w in workers:
            if w.step:
                w.remaining -= 1
                if not w.remaining:
                    # print('[%d] Worker %d done with step %s' % (time, w.id, w.step.id))
                    done.append(w.step.id)
                    w.step = None
                    w.remaining = None

            if not w.step:
                step = next(
                    (
                        s
                        for s in sorted(queue, key=lambda x: x.id)
                        if all(i.id in done for i in s.prevs)
                    ),
                    None,
                )

                if step:
                    # print('[%d] Worker %d taking step %s (%s)' % (time, w.id, step.id, [s.id for s in step.prevs]))
                    w.step = step
                    w.remaining = 61 + ord(step.id) - ord("A")

                    queue.remove(step)
                    queue += [s for s in step.nexts if s not in queue]

    print("Part 2 -> %d (%s)" % (time, "".join(done)))


if __name__ == "__main__":
    main()
