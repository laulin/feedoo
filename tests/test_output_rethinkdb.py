from feedoo.output.output_rethinkdb import OutputRethinkdb
from feedoo.event import Event
import unittest
from time import time

# # Enable those tests only if a rethinkDB is up
# IP = "172.17.0.1"
# class TestOutputRethinkdb(unittest.TestCase):
#     def test_1(self):
#         action = OutputRethinkdb("*", "timestamp", "sys-%Y%m%d", ip=IP)
#         event = Event("mytag", 123456789, {"timestamp":1603373121, "data":"aaaaaa"})
#         action.do(event)
#         action.finish()

#     def test_2(self):
#         action = OutputRethinkdb("*", "timestamp", "sys-%Y%m%d", ip=IP)
#         event_1 = Event("mytag", 1603373122, {"timestamp":1603373122, "data":"BBBB"})
#         action.do(event_1)
#         event_2 = Event("mytag", 1603373123,{"timestamp":1603373123, "data":"ccccc"})
#         action.do(event_2)
#         action.finish()

#     def test_force_flush(self):
#         action = OutputRethinkdb("*", "timestamp", "sys-%Y%m%d", buffer_size=1, ip=IP)
#         event_1 = Event("mytag", 1603373122, {"timestamp":1603373122, "data":"BBBB"})
#         action.do(event_1)
#         event_2 = Event("mytag", 1603373123,{"timestamp":1603373123, "data":"ccccc"})
#         action.do(event_2)

#     def test_timeout_update(self):
#         action = OutputRethinkdb("*", "timestamp", "sys-%Y%m%d", buffer_size=100, ip=IP)
#         event_1 = Event("mytag", 1603373122, {"timestamp":1603373122, "data":"BBBB"})
#         action.do(event_1)
#         event_2 = Event("mytag", 1603373123,{"timestamp":1603373123, "data":"ccccc"})
#         action.do(event_2)
#         def my_time():
#             return time() + 3600
#         action.update(my_time)








