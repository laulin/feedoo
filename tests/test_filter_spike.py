from feedoo.filter.filter_spike import FilterSpike
from feedoo.event import Event
import time
import unittest
import os
from pprint import pprint

def my_time(dt):
    def t():
        return time.time() + dt
    return t

TEST_DB = "/tmp/test.bin"
class TestFilterSpike(unittest.TestCase):
    def test_event_1(self):
        fs = FilterSpike(match="*",
                         tag="my_alert", 
                         alert={"title":"my alert", "priority":2}, 
                         spike_height=2, 
                         spike_type = "up", 
                         timeframe=60,
                         threshold_ref=1, 
                         threshold_cur=1)

        e = Event("tag", 123456789, {"type":"temp", "value":2})
        result = fs.do(e)
        expected = e

        self.assertEqual(result, expected)

    def test_event_2(self):
        fs = FilterSpike(match="*",
                         tag="my_alert", 
                         alert={"title":"my alert", "priority":2}, 
                         spike_height=2, 
                         spike_type = "up", 
                         timeframe=60,
                         threshold_ref=1, 
                         threshold_cur=1)

        e = Event("tag", 123456789, {"type":"temp", "value":2})
        fs.do(e, my_time(0))
        result = fs.do(e, my_time(70))
        expected = e

        self.assertEqual(result, expected)

    def test_event_up(self):
        fs = FilterSpike(match="*",
                         tag="my_alert", 
                         alert={"title":"my alert", "priority":2}, 
                         spike_height=2, 
                         spike_type = "up", 
                         timeframe=60,
                         threshold_ref=1, 
                         threshold_cur=1)

        e = Event("tag", 123456789, {"type":"temp", "value":2})
        fs.do(e, my_time(0))
        fs.do(e, my_time(70))
        fs.do(e, my_time(71))
        result = fs.do(e, my_time(72))
        #pprint(result)


        self.assertEqual(len(result), 2)

    def test_event_down_not(self):
        fs = FilterSpike(match="*",
                         tag="my_alert", 
                         alert={"title":"my alert", "priority":2}, 
                         spike_height=2, 
                         spike_type = "up", 
                         timeframe=60,
                         threshold_ref=1, 
                         threshold_cur=1)

        e = Event("tag", 123456789, {"type":"temp", "value":2})
        fs.do(e, my_time(0))
        fs.do(e, my_time(1))
        fs.do(e, my_time(2))
        result = fs.do(e, my_time(72))
        #pprint(result)
        expected = e


        self.assertEqual(result, expected)

    def test_event_both(self):
        fs = FilterSpike(match="*",
                         tag="my_alert", 
                         alert={"title":"my alert", "priority":2}, 
                         spike_height=2, 
                         spike_type = "both", 
                         timeframe=60,
                         threshold_ref=1, 
                         threshold_cur=1)

        e = Event("tag", 123456789, {"type":"temp", "value":2})
        fs.do(e, my_time(0))
        fs.do(e, my_time(1))
        fs.do(e, my_time(2))
        result = fs.do(e, my_time(72))
        #pprint(result)
        expected = 2


        self.assertEqual(len(result), expected)

    def test_keyed_event_up(self):
        fs = FilterSpike(match="*",
                         tag="my_alert", 
                         alert={"title":"my alert", "priority":2}, 
                         spike_height=2, 
                         spike_type = "up", 
                         timeframe=60,
                         threshold_ref=1, 
                         threshold_cur=1,
                         query_key="type")

        e = Event("tag", 123456789, {"type":"temp", "value":2})
        fs.do(e, my_time(0))
        e = Event("tag", 123456789, {"type":"cpu", "value":2})
        fs.do(e, my_time(70))
        fs.do(e, my_time(71))
        result = fs.do(e, my_time(72))
        #pprint(result)
        expected = e

        self.assertEqual(result, expected)

    def test_valued_event_up_not(self):
        fs = FilterSpike(match="*",
                         tag="my_alert", 
                         alert={"title":"my alert", "priority":2}, 
                         spike_height=2, 
                         spike_type = "up", 
                         timeframe=60,
                         threshold_ref=1, 
                         threshold_cur=1,
                         field_value="value")

        e = Event("tag", 123456789, {"type":"temp", "value":2})
        fs.do(e, my_time(0))
        e = Event("tag", 123456789, {"type":"cpu", "value":2})
        fs.do(e, my_time(70))
        fs.do(e, my_time(71))
        result = fs.do(e, my_time(72))
        #pprint(result)
        expected = e

        self.assertEqual(result, expected)

    def test_valued_event_up(self):
        fs = FilterSpike(match="*",
                         tag="my_alert", 
                         alert={"title":"my alert", "priority":2}, 
                         spike_height=2, 
                         spike_type = "up", 
                         timeframe=60,
                         threshold_ref=1, 
                         threshold_cur=1,
                         field_value="value")

        e = Event("tag", 123456789, {"type":"temp", "value":2})
        fs.do(e, my_time(0))
        e = Event("tag", 123456789, {"type":"cpu", "value":5})
        result = fs.do(e, my_time(72))
        # pprint(result)
        expected = 2

        self.assertEqual(len(result), expected)
        
    def test_valued_event_down(self):
        fs = FilterSpike(match="*",
                         tag="my_alert", 
                         alert={"title":"my alert", "priority":2}, 
                         spike_height=2, 
                         spike_type = "down", 
                         timeframe=60,
                         threshold_ref=1, 
                         threshold_cur=1,
                         field_value="value")

        e = Event("tag", 123456789, {"type":"cpu", "value":5})
        fs.do(e, my_time(0))
        e = Event("tag", 123456789, {"type":"temp", "value":2})
        result = fs.do(e, my_time(72))
        # pprint(result)
        expected = 2

        self.assertEqual(len(result), expected)

        

