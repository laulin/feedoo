from feedoo.filter.filter_frequency import FilterFrequency
from feedoo.event import Event
import time
import unittest
import os


TEST_DB = "/tmp/test.json"
class TestFilterFrequency(unittest.TestCase):
    def setUp(self):
        try:
            os.remove(TEST_DB)
        except:
            pass

    def test_low_frequency(self):
        ff = FilterFrequency(match="*", tag="alert", alert={"title":"alert !"}, num_events=2, timeframe=60)
        event = Event("log", 123456789, {"data":"xxxx"})
        result = ff.do(event)
        expected = event

        self.assertEqual(result, expected)

    def test_high_frequency(self):
        ff = FilterFrequency(match="*", tag="alert", alert={"title":"alert !"}, num_events=2, timeframe=60)
        event = Event("log", 123456789, {"data":"xxxx"})
        ff.do(event)
        event2 = Event("log", 123456790, {"data":"xxxx"})
        result = ff.do(event2)
        expected = 2
        # event + alerts
        self.assertEqual(len(result), expected)

    
    def test_low_frequency_query(self):
        ff = FilterFrequency(match="*", tag="alert", alert={"title":"alert !"}, num_events=2, timeframe=60, query_key="data")
        event = Event("log", 123456789, {"data":"xxxx"})
        result = ff.do(event)
        event2 = Event("log", 123456789, {"data":"yyyy"})
        result = ff.do(event2)
        expected = event2

        self.assertEqual(result, expected)

    def test_high_frequency_query(self):
        ff = FilterFrequency(match="*", tag="alert", alert={"title":"alert !"}, num_events=2, timeframe=60, query_key="data")
        event = Event("log", 123456789, {"data":"xxxx"})
        ff.do(event)
        event2 = Event("log", 123456789, {"data":"yyyy"})
        ff.do(event2)
        event3 = Event("log", 123456789, {"data":"xxxx"})
        result = ff.do(event3)
        expected = 2

        self.assertEqual(len(result), expected)

    def test_update(self):
        ff = FilterFrequency(match="*", tag="alert", alert={"title":"alert !"}, num_events=2, timeframe=60)
        event = Event("log", 123456789, {"data":"xxxx"})
        ff.do(event)

        # time elapsed : 1H, no more event in timeframe
        def time_mock():
            return time.time() + 3600
        ff.update(time_mock)

        event2 = Event("log", 123456790, {"data":"xxxx"})
        result = ff.do(event2)
        expected = event2

        self.assertEqual(result, expected)
    