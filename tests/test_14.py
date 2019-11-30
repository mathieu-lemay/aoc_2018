from unittest import TestCase

from d14 import get_next_scores, get_recipes_before


class Test14(TestCase):
    def test_get_next_scores(self):
        params = (
            (5, "0124515891"),
            (9, "5158916779"),
            (18, "9251071085"),
            (2018, "5941429882"),
        )

        for n, expected in params:
            with self.subTest(n=n, expected=expected):
                self.assertEqual(expected, get_next_scores(n))

    def test_get_recipes_before(self):
        params = (
            ("01245", 5),
            ("51589", 9),
            ("92510", 18),
            ("59414", 2018),
        )

        for n, expected in params:
            with self.subTest(n=n, expected=expected):
                self.assertEqual(expected, get_recipes_before(n))
