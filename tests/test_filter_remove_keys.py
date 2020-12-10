from feedo.filter.filter_remove_keys import FilterRemoveKeys
from feedo.event import Event
import unittest

class TestFilterRemoveKeys(unittest.TestCase):
    def test_1(self):
        action = FilterRemoveKeys("*", "a")
        event = Event("my_tag", 123456789, {"a": "b", "c":"d"})
        result = action.do(event)
        expected = {"c":"d"}

        self.assertEqual(result.record, expected)

    def test_2(self):
        action = FilterRemoveKeys("*", ["a", "c"])
        event = Event("my_tag", 123456789, {"a": "b", "c":"d"})
        result = action.do(event)
        expected = {}

        self.assertEqual(result.record, expected)

    def test_3(self):
        action = FilterRemoveKeys("*", "z")
        event = Event("my_tag", 123456789, {"a": "b", "c":"d"})
        result = action.do(event)
        expected = {"a": "b", "c":"d"}

        self.assertEqual(result.record, expected)

    def test_4(self):
        action = FilterRemoveKeys("*", ["a", "z"])
        event = Event("my_tag", 123456789, {"a": "b", "c":"d"})
        result = action.do(event)
        expected = {"c":"d"}

        self.assertEqual(result.record, expected)
