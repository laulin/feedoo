from feedoo.filter.filter_spike import FilterSpike
from feedoo.event import Event
import time
import unittest
import os


TEST_DB = "/tmp/test.bin"
class TestFilterSpike(unittest.TestCase):
    def setUp(self):
        try:
            os.remove(TEST_DB)
        except:
            pass
