#! /usr/bin/env python

import os.path
from time import time

_id = 0


class Node:
    def __init__(self, id_):
        self.id = id_
        self.nb_child = None
        self.nb_metadata = None
        self.parent = None
        self.children = []
        self.metadata = []

    def __repr__(self):
        cname = self.__class__.__name__
        attrs = ', '.join('%s=%s' % (k, v) for k, v in self.__dict__.items() if type(v) == int)
        return '<%s(%s)>' % (cname, attrs)


def main():
    raw_data = ''
    with open(os.path.join('input', '08.txt')) as f:
        buffer = f.read(2048)
        while buffer:
            raw_data += buffer
            buffer = f.read(2048)

    data = [int(i) for i in raw_data.split(' ')]

    global _id
    root = Node(_id)
    _id += 1

    root.nb_child = data[0]
    root.nb_metadata = data[1]
    p = 2
    read_node(root, data, p)

    print('Part 1 -> %d' % sum_meta(root))
    print('Part 2 -> %d' % sum_meta2(root))


def read_node(node, data, p):
    global _id

    for _ in range(node.nb_child):
        c = Node(_id)
        node.children.append(c)
        _id += 1

        c.nb_child = data[p]
        c.nb_metadata = data[p+1]

        p = read_node(c, data, p+2)

    for i in range(node.nb_metadata):
        node.metadata.append(data[p+i])

    return p + node.nb_metadata


def sum_meta(node):
    s = sum(node.metadata)

    for c in node.children:
        s += sum_meta(c)

    return s


def sum_meta2(node):
    if not node.children:
        return sum(node.metadata)

    s = 0
    for i in node.metadata:
        if 0 < i <= node.nb_child:
            s += sum_meta2(node.children[i-1])

    return s


if __name__ == '__main__':
    ts = time()
    main()
    ts = time() - ts
    print('Done in %.3fms' % (ts * 1000))
