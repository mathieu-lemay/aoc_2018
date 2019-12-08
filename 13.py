#! /usr/bin/env python

import os.path
from enum import Enum
from time import time


class Direction(Enum):
    # Rail
    ALL = "+"
    UD = "|"
    LR = "-"
    LD_UR = "\\"
    LU_DR = "/"

    # Cart
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

    # Nothing
    NONE = " "


class Element:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def __repr__(self):
        return self.direction.value


class Rail(Element):
    pass


class Cart(Element):
    def __init__(self, id_, x, y, direction):
        super(Cart, self).__init__(x, y, direction)
        self.id = id_
        self.next_turn = Direction.LEFT
        self.crashed = False

    def move(self, rails):
        d = get_dir_delta(self.direction)

        self.x += d[0]
        self.y += d[1]

        cur_rail = get_rail(rails, self.x, self.y)
        if cur_rail.direction == Direction.ALL:
            self.turn()
        elif cur_rail.direction == Direction.LD_UR:
            self.direction = {
                Direction.LEFT: Direction.UP,
                Direction.UP: Direction.LEFT,
                Direction.RIGHT: Direction.DOWN,
                Direction.DOWN: Direction.RIGHT,
            }[self.direction]
        elif cur_rail.direction == Direction.LU_DR:
            self.direction = {
                Direction.LEFT: Direction.DOWN,
                Direction.DOWN: Direction.LEFT,
                Direction.RIGHT: Direction.UP,
                Direction.UP: Direction.RIGHT,
            }[self.direction]

    def turn(self):
        if self.next_turn == Direction.LEFT:
            self.direction = {
                Direction.LEFT: Direction.DOWN,
                Direction.DOWN: Direction.RIGHT,
                Direction.RIGHT: Direction.UP,
                Direction.UP: Direction.LEFT,
            }[self.direction]
        elif self.next_turn == Direction.RIGHT:
            self.direction = {
                Direction.LEFT: Direction.UP,
                Direction.UP: Direction.RIGHT,
                Direction.RIGHT: Direction.DOWN,
                Direction.DOWN: Direction.LEFT,
            }[self.direction]

        self.next_turn = {
            Direction.LEFT: Direction.ALL,
            Direction.ALL: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }[self.next_turn]


def get_dir_delta(direction):
    return {
        Direction.UP: (0, -1),
        Direction.DOWN: (0, 1),
        Direction.LEFT: (-1, 0),
        Direction.RIGHT: (1, 0),
        None: (0, 0),
    }[direction]


def get_rail(rails, x, y, offset=None):
    d = get_dir_delta(offset)

    x = x + d[0]
    y = y + d[1]

    if x < 0 or y < 0:
        return None

    try:
        return rails[y][x]
    except IndexError:
        return None


def fill_rail_at(rails, x, y):
    _u = _d = _l = _r = 0

    r_u = get_rail(rails, x, y, Direction.UP)
    r_d = get_rail(rails, x, y, Direction.DOWN)
    r_l = get_rail(rails, x, y, Direction.LEFT)
    r_r = get_rail(rails, x, y, Direction.RIGHT)

    if r_u and r_u.direction != Direction.LR and r_u.direction != Direction.NONE:
        _u = 1

    if r_d and r_d.direction != Direction.LR and r_d.direction != Direction.NONE and r_d.direction != Direction.LU_DR:
        _d = 1

    if r_l and r_l.direction != Direction.UD and r_l.direction != Direction.NONE:
        _l = 1

    if r_r and r_r.direction != Direction.UD and r_r.direction != Direction.NONE:
        _r = 1

    direction = {
        (1, 1, 1, 1): Direction.ALL,
        (1, 1, 0, 0): Direction.UD,
        (0, 0, 1, 1): Direction.LR,
        (0, 1, 1, 0): Direction.LD_UR,
        (1, 0, 0, 1): Direction.LD_UR,
        (1, 0, 1, 0): Direction.LU_DR,
        (0, 1, 0, 1): Direction.LU_DR,
    }[(_u, _d, _l, _r)]

    rails[y][x] = Rail(x, y, direction)


def main():
    rails = []
    carts = []

    with open(os.path.join("input", "13.txt")) as f:
        y = 0
        c_id = 1
        for l in f.readlines():
            rr = []
            for x, c in enumerate(l):
                if c in "|-/\\+ ":
                    rr.append(Rail(x, y, Direction(c)))
                else:
                    rr.append(Rail(x, y, Direction.NONE))

                if c in "^v<>":
                    carts.append(Cart(c_id, x, y, Direction(c)))
                    c_id += 1

            rails.append(rr)
            y += 1

    for c in carts:
        fill_rail_at(rails, c.x, c.y)

    nb_crash = 0
    ticks = 0
    nb_carts = len(carts)
    while nb_carts > 1:
        ticks += 1

        for cart in sorted(carts, key=lambda c: (c.y, c.x)):
            if cart.crashed:
                continue

            cart.move(rails)
            other = next(
                (
                    c
                    for c in carts
                    if c.id != cart.id
                    and not c.crashed
                    and (c.x, c.y) == (cart.x, cart.y)
                ),
                None,
            )

            if other:
                if not nb_crash:
                    print("Part 1: %d,%d (ticks=%d)" % (cart.x, cart.y, ticks))

                cart.crashed = True
                other.crashed = True
                nb_carts = len([c for c in carts if not c.crashed])
                nb_crash += 1

                print(
                    "Crash! Carts %d / %d at (%d,%d). Carts left: %d"
                    % (cart.id, other.id, cart.x, cart.y, nb_carts)
                )

    uncrashed = [c for c in carts if not c.crashed]
    if len(uncrashed) != 1:
        raise ValueError("More than one uncrashed cart")

    c = uncrashed[0]
    if not c.crashed:
        print("Part 2: %d,%d (ticks=%d)" % (c.x, c.y, ticks))


if __name__ == "__main__":
    ts = time()
    main()
    ts = time() - ts
    print("Done in %.3fms" % (ts * 1000))
