from feedoo.filter.filter_flatline import FilterFlatline
from feedoo.event import Event
import time
import unittest
import os

def my_time(dt):
    def t():
        return time.time() + dt
    return t


class TestFilterFlatline(unittest.TestCase):
    def test_1(self):
        ffl = FilterFlatline(match='*', 
                                tag='my_log', 
                                alert = {"title":"No heart beat", "priority":1}, 
                                threshold = 1, 
                                timeframe=60, 
                                query_key=None, 
                                forget_keys=True)

        event = Event("my_log", 123456789, {"type":"hearbeat"})
        ffl.do(event, my_time(10))
        result = ffl.update(my_time(65))

        expected = []
        self.assertEqual(result, expected)

    def test_2(self):
        ffl = FilterFlatline(match='*', 
                                tag='my_log', 
                                alert = {"title":"No heart beat", "priority":1}, 
                                threshold = 1, 
                                timeframe=60, 
                                query_key=None, 
                                forget_keys=True)

        event = Event("my_log", 123456789, {"type":"hearbeat"})
        ffl.do(event, my_time(10))
        ffl.update(my_time(60))
        result = ffl.update(my_time(120))
        expected = 1
        self.assertEqual(len(result), expected)

    def test_3(self):
        ffl = FilterFlatline(match='*', 
                                tag='my_log', 
                                alert = {"title":"No heart beat", "priority":1}, 
                                threshold = 2, 
                                timeframe=60, 
                                query_key="type", 
                                forget_keys=True)

        event = Event("my_log", 123456789, {"type":"hearbeat"})
        ffl.do(event, my_time(10))
        event = Event("my_log", 123456789, {"type":"ping"})
        ffl.do(event, my_time(111))
        ffl.update(my_time(60))
        result = ffl.update(my_time(120))
        expected = 2
        self.assertEqual(len(result), expected)

    def test_4(self):
        # do not forget key so keep going to emit alerts
        ffl = FilterFlatline(match='*', 
                                tag='my_log', 
                                alert = {"title":"No heart beat", "priority":1}, 
                                threshold = 2, 
                                timeframe=60, 
                                query_key="type", 
                                forget_keys=False)

        event = Event("my_log", 123456789, {"type":"hearbeat"})
        ffl.do(event, my_time(10))
        ffl.update(my_time(60))
        ffl.update(my_time(120))
        result = ffl.update(my_time(180))
        expected = 1
        self.assertEqual(len(result), expected)
