import logging
import unittest
from feedoo.input.input_forward import InputForward
from feedoo.event import Event
from unittest.mock import Mock

class Next:
    def __init__(self):
        self.events = []

    def receive(self, event):
        self.events.append(event)

class TestInputForward(unittest.TestCase):
    def test_init(self):
        forward = InputForward(_start_server=False)


    def test_callback(self):
        forward = InputForward(_start_server=False)
        e = Event(b"my.tag", 123456789, {"log":"test"})
        forward.callback(e)
        forward.finish()


    def test_format_record(self):
        next_action = Next()
        forward = InputForward(_start_server=False)
        forward.set_next(next_action)
        e = Event(b"my.tag", 123456789, {b"log":b"test", b"timestamp":123456789, b"temp":33.56})
        forward.callback(e)
        forward.update()
        
        result = next_action.events[0]
        expected = Event("my.tag", 123456789, {"log":"test", "timestamp":123456789, "temp":33.56})
        forward.finish()
        self.assertEqual(result, expected)