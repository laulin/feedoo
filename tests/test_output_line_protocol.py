import shutil
import unittest
from feedoo.output.output_line_protocol import OutputLineProtocol
from feedoo.event import Event
from time import time

class TestOutputLineProtocol(unittest.TestCase):
    def tearDown(self):
        shutil.rmtree("/tmp/archive/")

    def test_1(self):
        action = OutputLineProtocol("*", "timestamp", "my_mez", ["source"], ["data", "tick"], "/tmp/archive/{source}/sys-%Y%m%d")
        event_1 = Event("my_tag", 1603373121, {"timestamp":1603373121, "data":"aaaaaa", "tick":10, "source":"j2"})
        action.do(event_1)
        action.finish()
        with open("/tmp/archive/j2/sys-20201022") as f:
            result = f.read()
            
        expected = 'my_mez,source=j2 data="aaaaaa",tick=10 1603373121000\n'
        self.assertEqual(result, expected)








