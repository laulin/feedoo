from feedo.action_retag import ActionRetag
from feedo.event import Event
import unittest

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







