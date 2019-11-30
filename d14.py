#! /usr/bin/env pypy3


class RecipeTracker:
    def __init__(self, recipes):
        self.recipes = recipes
        self.elves = [0, 1]
        self._cursor = 0

    def craft_next_recipes(self):
        n = sum(self.recipes[e] for e in self.elves)

        if n >= 10:
            self._add_recipe(n // 10)
            self._add_recipe(n % 10)
        else:
            self._add_recipe(n)

    def _add_recipe(self, n):
        self.recipes.append(n)

    def move_elves(self):
        nb_r = len(self.recipes)
        for i, e in enumerate(self.elves):
            new_idx = e + self.recipes[e] + 1

            if new_idx >= nb_r:
                new_idx %= nb_r

            self.elves[i] = new_idx

    def get_ten_after(self, n):
        if len(self.recipes) > (n + 10):
            return self.recipes[n : n + 10]

        return None

    def search_for(self, seq):
        idx = 0
        for c in range(self._cursor, len(self.recipes)):
            if self.recipes[c] == seq[idx]:
                idx += 1

                if idx == len(seq):
                    return c - idx + 1
            else:
                self._cursor = c
                idx = 0

        return None


def get_next_scores(n):
    rt = RecipeTracker([3, 7])
    while True:
        rt.craft_next_recipes()
        rt.move_elves()

        n10 = rt.get_ten_after(n)

        if n10:
            return "".join(str(i) for i in n10)


def get_recipes_before(n):
    search = [int(c) for c in n]
    rt = RecipeTracker([3, 7])

    while True:
        rt.craft_next_recipes()
        rt.move_elves()
        x = rt.search_for(search)
        if x:
            return x


if __name__ == "__main__":
    from time import time as ts

    _input = 327901

    _t = ts()

    print(f"Part 1: {get_next_scores(_input)}", flush=True)
    print(f"Part 2: {get_recipes_before(str(_input))}")

    _t = ts() - _t
    print(f"\nDone in {_t:.3f}s")
