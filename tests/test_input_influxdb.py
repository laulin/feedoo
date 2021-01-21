import logging
import unittest
from feedoo.input.input_influxdb import InputInfluxdb
from feedoo.event import Event
from unittest.mock import Mock

class Next:
    def __init__(self):
        self.events = []

    def receive(self, event):
        self.events.append(event)

class TestInputInfluxdb(unittest.TestCase):
    def test_1(self):
        
        influx = InputInfluxdb("netflow", "SELECT * FROM netflow WHERE time > now() - 1m")

