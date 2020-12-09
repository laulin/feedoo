import json
from abstract_action import AbstractAction
from event import Event
import unittest

# remove one or more keys of the document

class ActionRemoveKeys(AbstractAction):
    def __init__(self, match, keys):
        AbstractAction.__init__(self, match)
        self._keys = keys

    def do(self, event):
        record = dict(event.record)
        # if string
        if isinstance(self._keys, str):
            if self._keys in record:
                del record[self._keys]
        # if list/tuple
        else:
            for k in self._keys:
                if k in record:
                    del record[k]
                
        return Event(event.tag, event.timestamp, record)


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






