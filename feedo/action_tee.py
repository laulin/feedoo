from chronyk import Chronyk
from abstract_action import AbstractAction
from event import Event
import unittest

# duplicate event with a new tag

class ActionTee(AbstractAction):
    def __init__(self, match, new_tag):
        AbstractAction.__init__(self, match)
        self._tag = new_tag

    def do(self, event):
        return [Event(event.tag, event.timestamp, event.record), Event(self._tag, event.timestamp, event.record)]



class TestActionTee(unittest.TestCase):
    def test_1(self):
        action = ActionTee("*", "t")
        event = Event("my_tag", 123456789, {"t": "2020-10-22T08:50:20+00:00"})
        result = action.do(event)
        

        self.assertEqual(len(result), 2)







