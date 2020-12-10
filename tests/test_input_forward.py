import logging
import unittest
from feedo.input.input_forward import InputForward
from feedo.event import Event
from unittest.mock import Mock

class TestInputForward(unittest.TestCase):
    def test_init(self):
        forward = InputForward()
        forward.finish()

    def test_init(self):
        forward = InputForward()
        e = Event("my.tag", 123456789, {"log":"test"})
        forward.callback(e)
        forward.finish()