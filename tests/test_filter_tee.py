from feedo.filter.filter_tee import FilterTee
from feedo.event import Event
import unittest

class TestFilterTee(unittest.TestCase):
    def test_1(self):
        action = FilterTee("*", "t")
        event = Event("my_tag", 123456789, {"t": "2020-10-22T08:50:20+00:00"})
        result = action.do(event)
        

        self.assertEqual(len(result), 2)







