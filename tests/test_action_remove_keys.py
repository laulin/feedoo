from feedo.action_remove_keys import ActionRemoveKeys
from feedo.event import Event
import unittest

class TestActionRemoveKeys(unittest.TestCase):
    def test_1(self):
        action = ActionRemoveKeys("*", "a")
        event = Event("my_tag", 123456789, {"a": "b", "c":"d"})
        result = action.do(event)
        expected = {"c":"d"}

        self.assertEqual(result.record, expected)

    def test_2(self):
        action = ActionRemoveKeys("*", ["a", "c"])
        event = Event("my_tag", 123456789, {"a": "b", "c":"d"})
        result = action.do(event)
        expected = {}

        self.assertEqual(result.record, expected)

    def test_3(self):
        action = ActionRemoveKeys("*", "z")
        event = Event("my_tag", 123456789, {"a": "b", "c":"d"})
        result = action.do(event)
        expected = {"a": "b", "c":"d"}

        self.assertEqual(result.record, expected)

    def test_4(self):
        action = ActionRemoveKeys("*", ["a", "z"])
        event = Event("my_tag", 123456789, {"a": "b", "c":"d"})
        result = action.do(event)
        expected = {"c":"d"}

        self.assertEqual(result.record, expected)
