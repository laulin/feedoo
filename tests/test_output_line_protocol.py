import shutil
import unittest
from feedoo.output.output_line_protocol import OutputLineProtocol
from feedoo.event import Event
from time import time

def absolute_time(ts):
    def _time():
        return ts
    return _time

class TestOutputLineProtocol(unittest.TestCase):
    def tearDown(self):
        shutil.rmtree("/tmp/archive/")

    def test_1(self):
        action = OutputLineProtocol("*", "my_mez", ["source"], ["data", "tick"], "/tmp/archive/{source}/sys-%Y%m%d", "timestamp")
        event_1 = Event("my_tag", 1603373121, {"timestamp":1603373121, "data":"aaaaaa", "tick":10, "source":"j2"})
        action.do(event_1)
        action.finish()
        with open("/tmp/archive/j2/sys-20201022") as f:
            result = f.read()
            
        expected = 'my_mez,source=j2 data="aaaaaa",tick=10 1603373121000000000\n'
        self.assertEqual(result, expected)

    def test_2(self):
        action = OutputLineProtocol("*", "my_mez", ["source"], ["data", "tick"], "/tmp/archive/{source}/sys-%Y%m%d", None)
        event_1 = Event("my_tag", 1603373121, {"timestamp":1603373121, "data":"aaaaaa", "tick":10, "source":"j2"})
        action.do(event_1, absolute_time(1603373121))
        action.finish(absolute_time(1603373121))
        with open("/tmp/archive/j2/sys-20201022") as f:
            result = f.read()
            
        expected = 'my_mez,source=j2 data="aaaaaa",tick=10 1603373121000000000\n'
        self.assertEqual(result, expected)








