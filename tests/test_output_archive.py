import shutil
import unittest
from feedoo.output.output_archive import OutputArchive
from feedoo.event import Event
from time import time

class TestOutputArchive(unittest.TestCase):
    def tearDown(self):
        shutil.rmtree("/tmp/archive/")

    def test_1(self):
        action = OutputArchive("*", "timestamp", "/tmp/archive/{source}/sys-%Y%m%d")
        event_1 = Event("my_tag", 1603373121, {"timestamp":1603373121, "data":"aaaaaa", "source":"j2"})
        action.do(event_1)
        action.finish()
        with open("/tmp/archive/j2/sys-20201022") as f:
            data = f.read()
        

    def test_2(self):
        action = OutputArchive("*", "timestamp", "/tmp/archive/{source}/sys-%Y%m%d")
        event_1 = Event("my_tag", 1603373122, {"timestamp":1603373122, "data":"BBBB", "source":"j2"})
        event_2 = Event("my_tag", 1603373123, {"timestamp":1603373123, "data":"ccccc", "source":"j2"})
        action.do(event_1)
        action.do(event_2)
        action.finish()
        with open("/tmp/archive/j2/sys-20201022") as f:
            data = f.read()

    def test_force_flush(self):
        action = OutputArchive("*", "timestamp", "/tmp/archive/{source}/sys-%Y%m%d", buffer_size=1)
        event_1 = Event("my_tag", 1603373122, {"timestamp":1603373122, "data":"ddd", "source":"j2"})
        event_2 = Event("my_tag", 1603373123, {"timestamp":1603373123, "data":"eee", "source":"j2"})
        action.do(event_1)
        action.do(event_2) # pushed because buffer is full
        with open("/tmp/archive/j2/sys-20201022") as f:
            data = f.read()

    def test_existing_dir(self):
        action = OutputArchive("*", "timestamp", "/tmp/archive/{source}/sys-%Y%m%d", buffer_size=1)
        event_1 = Event("my_tag", 1603373122, {"timestamp":1603373122, "data":"ddd", "source":"j2"})
        event_2 = Event("my_tag", 1603373123, {"timestamp":1603373123, "data":"eee", "source":"j2"})
        event_3 = Event("my_tag", 1603373122, {"timestamp":1603373124, "data":"ff", "source":"j2"})
        event_4 = Event("my_tag", 1603373123, {"timestamp":1603373125, "data":"gg", "source":"j2"})
        action.do(event_1)
        action.do(event_2)
        action.do(event_3)
        action.do(event_4) 

    def test_timeout(self):
        action = OutputArchive("*", "timestamp", "/tmp/archive/{source}/sys-%Y%m%d", buffer_size=1)
        event_1 = Event("my_tag", 1603373122, {"timestamp":1603373122, "data":"ddd", "source":"j2"})
        action.do(event_1)
        def my_time():
            return time() + 3600
        action.update(my_time)
        with open("/tmp/archive/j2/sys-20201022") as f:
            data = f.read()









