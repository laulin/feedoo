from chronyk import Chronyk
from abstract_action import AbstractAction
from event import Event
import unittest

# retag an event with contant value or key

class ActionRetag(AbstractAction):
    def __init__(self, match, value, key=None):
        AbstractAction.__init__(self, match)
        self._value = value
        self._key = key

    def do(self, event):
        record = event.record
        new_tag = record.get(self._key, self._value)
        return Event(new_tag, event.timestamp, event.record)



class TestActionRetag(unittest.TestCase):
    def test_1(self):
        action = ActionRetag("*", "t")
        event = Event("my_tag", 123456789, {"t": "2020-10-22T08:50:20+00:00"})
        result = action.do(event)
        

        self.assertEqual(result.tag, "t")

    def test_2(self):
        action = ActionRetag("*", "t", "g")
        event = Event("my_tag", 123456789, {"t": "2020-10-22T08:50:20+00:00", "g":"new_tag"})
        result = action.do(event)
        

        self.assertEqual(result.tag, "new_tag")

    def test_3(self):
        action = ActionRetag("*", "x", "g")
        event = Event("my_tag", 123456789, {"t": "2020-10-22T08:50:20+00:00"})
        result = action.do(event)
        

        self.assertEqual(result.tag, "x")







