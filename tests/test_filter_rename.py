from feedoo.filter.filter_rename import FilterRename
from feedoo.event import Event
import unittest

# parse a date field and transform it

class TestFilterRename(unittest.TestCase):
    def test_1(self):
        action = FilterRename("*", {"t": "x"})
        event = Event("my_tag", 123456789, {"t": "aaaa"})
        result = action.do(event)
        expected = {"x": "aaaa"}

        self.assertEqual(result.record, expected)

    def test_2(self):
        action = FilterRename("*", {"t": "x", "u":"b"})
        event = Event("my_tag", 123456789, {"t": "aaaa"})
        result = action.do(event)
        expected = {"x": "aaaa"}

        self.assertEqual(result.record, expected)






