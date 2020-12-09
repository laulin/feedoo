from chronyk import Chronyk
from abstract_action import AbstractAction
from event import Event
import unittest

# parse a date field and transform it

class ActionDate(AbstractAction):
    def __init__(self, match, key, format=None):
        AbstractAction.__init__(self, match)
        self._key = key
        self._format = format

    def do(self, event):
        record = dict(event.record)
        time = Chronyk(record[self._key])
        if self._format is None:
            record[self._key] = time.timestamp()
        else:
            record[self._key] = time.timestring(self._format)

        return Event(event.tag, event.timestamp, record)



class TestActionDate(unittest.TestCase):
    def test_1(self):
        action = ActionDate("*", "t")
        event = Event("my_tag", 123456789, {"t": "2020-10-22T08:50:20+00:00"})
        result = action.do(event)
        expected = {"t": 1603356620.0}

        self.assertEqual(result.record, expected)

    def test_2(self):
        action = ActionDate("*", "t", "%Y-%m-%d")
        event = Event("my_tag", 123456789, {"t": 1603356620.0})
        result = action.do(event)
        expected = {"t": "2020-10-22"}

        self.assertEqual(result.record, expected)






