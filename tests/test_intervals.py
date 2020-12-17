import unittest
from feedoo.intervals import * # ok for testing

class TestInterval(unittest.TestCase):
    def test_1(self):
        result = raw_window(5, 14, 3)
        expected = [(5, 7), (8, 10), (11, 13), (14, 16)]
        self.assertEqual(result, expected)

    def test_2(self):
        result = clamped_window(5, 14, 3)
        expected = [(5, 7), (8, 10), (11, 13), (14, 14)]
        self.assertEqual(result, expected)

    def test_3(self):
        result = intersect(1, 3, 4, 6)
        expected = None, None
        self.assertEqual(result, expected)

    def test_4(self):
        result = intersect(1, 5, 4, 6)
        expected = (4,5)
        self.assertEqual(result, expected)

    def test_5(self):
        result = intersect(5, 7, 4, 6)
        expected = (5,6)
        self.assertEqual(result, expected)

    def test_6(self):
        result = intersect(0, 10, 4, 6)
        expected = (4,6)
        self.assertEqual(result, expected)

    def test_7(self):
        segments = [
            (5,14),
            (15,24)
        ]
        result = iterate_intervals(0,19,3,segments)
        expected = [
            [(5, 7), (8, 10), (11, 13), (14, 14)], 
            [(15, 17), (18, 19)]
        ]
        self.assertEqual(result, expected)