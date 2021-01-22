from feedoo.filter.filter_groupby import FilterGroupby
from feedoo.event import Event
import unittest
from unittest.mock import Mock

def absolute_time(ts):
    def _time():
        return ts
    return _time

class TestFilterGroupby(unittest.TestCase):
    def test_1(self):
        action = FilterGroupby("*", "grouped", ["a", "b"], ["c"])
        next_action = Mock()
        action.set_next(next_action)

        event = Event("my_tag", 123456789, {"a": "x", "b" : "y", "c" : "aaa" })
        action.do(event)
        action.update(absolute_time(1))
        expected = Event(tag='grouped', timestamp=1, record={'a': 'x', 'b': 'y', 'value': [{'c': 'aaa'}]})
        next_action.receive.assert_called_with(expected)

    def test_unique(self):
        action = FilterGroupby("*", "grouped", ["a", "b"], ["c"], unique=True)
        next_action = Mock()
        action.set_next(next_action)

        event = Event("my_tag", 123456789, {"a": "x", "b" : "y", "c" : "aaa" })
        action.do(event)
        event = Event("my_tag", 123456789, {"a": "x", "b" : "y", "c" : "aaa" })
        action.do(event)
        action.update(absolute_time(1))
        expected = Event(tag='grouped', timestamp=1, record={'a': 'x', 'b': 'y', 'value': [{'c': 'aaa'}]})
        next_action.receive.assert_called_with(expected)

    def test_unique_2(self):
        action = FilterGroupby("*", "grouped", ["a", "b"], ["c"], unique=True)
        next_action = Mock()
        action.set_next(next_action)

        event = Event("my_tag", 123456789, {"a": "x", "b" : "y", "c" : "aaa" })
        action.do(event)
        event = Event("my_tag", 123456789, {"a": "x", "b" : "y", "c" : "aaa" })
        action.do(event)
        event = Event("my_tag", 123456789, {"a": "x", "b" : "y", "c" : "ddd" })
        action.do(event)
        action.update(absolute_time(1))
        expected = Event(tag='grouped', timestamp=1, record={'a': 'x', 'b': 'y', 'value': [{'c': 'aaa'}, {'c': 'ddd'}]})
        next_action.receive.assert_called_with(expected)

    def test_count(self):
        action = FilterGroupby("*", "grouped", ["a", "b"], ["c"], unique=True, count=True)
        next_action = Mock()
        action.set_next(next_action)

        event = Event("my_tag", 123456789, {"a": "x", "b" : "y", "c" : "aaa" })
        action.do(event)
        event = Event("my_tag", 123456789, {"a": "x", "b" : "y", "c" : "aaa" })
        action.do(event)
        action.update(absolute_time(1))
        expected = Event(tag='grouped', timestamp=1, record={'a': 'x', 'b': 'y', 'value': 1})
        next_action.receive.assert_called_with(expected)

    def test_count_2(self):
        action = FilterGroupby("*", "grouped", ["a", "b"], ["c"], unique=False, count=True)
        next_action = Mock()
        action.set_next(next_action)

        event = Event("my_tag", 123456789, {"a": "x", "b" : "y", "c" : "aaa" })
        action.do(event)
        event = Event("my_tag", 123456789, {"a": "x", "b" : "y", "c" : "aaa" })
        action.do(event)
        action.update(absolute_time(1))
        expected = Event(tag='grouped', timestamp=1, record={'a': 'x', 'b': 'y', 'value': 2})
        next_action.receive.assert_called_with(expected)







