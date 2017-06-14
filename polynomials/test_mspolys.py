import unittest
import hypothesis
import hypothesis.strategies as st
from mspolys import Polynomial as Poly 

liststrat = st.lists(st.integers() | st.floats())
dictstrat = st.dictionaries(st.integers(min_value=0, max_value=20),
                            st.integers() | st.floats(), max_size=10)


class PolyCase(unittest.TestCase):
    def testAcceptsNone(self):
        try:
            Poly()
        except Exception as e:
            self.fail(e)

    @hypothesis.given(liststrat)
    def testAcceptsList(self, l):
        try:
            Poly(l)
        except Exception as e:
            self.fail("Poly() raised {} unexpectedly!".format(e))

    @hypothesis.given(dictstrat)
    def testAcceptsDict(self, d):
        try:
            d, Poly(d)
        except Exception as e:
            print(e)

    def testPretty(self):
        pretty_tests = {
            (4, 3, 2): '4x^2 + 3x + 2',
            (2, 8, 3): '2x^2 + 8x + 3',
            (8, 6, 7, 9): '8x^3 + 6x^2 + 7x + 9',
            (7, -3, 5, -6): '7x^3 - 3x^2 + 5x - 6',
            (5, 0, 2): '5x^2 + 2',
            (-7, 0, 3, 5, 0, -2): '-7x^5 + 3x^3 + 5x^2 - 2',
            (-7, 0, 0, 5, 0, 0): '-7x^5 + 5x^2',
        }
        for test, string in pretty_tests.items():
            self.assertEqual(str(Poly(test)), string)

    def testEquality(self):
        self.assertEqual(Poly(), Poly())
        self.assertEqual(Poly((3, 4, 5)), Poly((3, 4, 5)))
        self.assertNotEqual(Poly((5, 4, 3)), Poly((3, 4, 5)))
        self.assertEqual(Poly((7, 8, 3, 2, 9)), Poly((7, 8, 3, 2, 9)))

    def testAdd(self):
        self.assertEqual(Poly((3,)) + Poly((2,)), Poly((5,)))
        self.assertEqual(Poly((3, 1, 2)) + Poly((1, 2, 3)), Poly((4, 3, 5)))
        self.assertEqual(Poly((15, 16, 19, 18)) + Poly((11, 19)),
                         Poly((15, 16, 30, 37)))

    def testMul(self):
        self.assertEqual(Poly((4, -5)) * Poly((2, 3, -6)),
                         Poly((8, 2, -39, 30)))
        self.assertEqual(Poly((3, 2)) * Poly((4, -7, 5)),
                         Poly((12, -13, 1, 10)))

    @hypothesis.given(dictstrat | liststrat)
    def testDict(self, o1):
        p1 = Poly(o1)
        p2 = Poly(p1.todict())
        self.assertEqual(p1, p2)


unittest.main(argv=['first-arg-is-ignored'], exit=False)
