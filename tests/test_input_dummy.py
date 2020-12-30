import logging
import unittest
from feedoo.input.input_dummy import InputDummy
from feedoo.event import Event
from unittest.mock import Mock

class Next:
    def __init__(self):
        self.events = []

    def receive(self, event):
        self.events.append(event)

class TestInputDummy(unittest.TestCase):
    def test_repeat_1(self):
        next_action = Next()
        dummy = InputDummy("mytag", {"data":1})
        dummy.set_next(next_action)
        dummy.update()

        self.assertEqual(len(next_action.events), 1)

    def test_repeat_10(self):
        next_action = Next()
        dummy = InputDummy("mytag", {"data":1}, 10)
        dummy.set_next(next_action)
        for i in range(12):
            dummy.update()

        self.assertEqual(len(next_action.events), 10)

    def test_repeat_5x2(self):
        next_action = Next()
        dummy = InputDummy("mytag", [{"data":1}, {"data":2}], 5)
        dummy.set_next(next_action)
        for i in range(6):
            dummy.update()

        self.assertEqual(len(next_action.events), 10)

