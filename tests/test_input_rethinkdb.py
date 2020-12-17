from feedoo.input.input_rethinkdb import InputRethinkdb
from feedoo.rethinkdb_adapter import RethinkdbAdapter
import unittest
import os
import logging
from pprint import pprint
from rethinkdb import r as Rethinkdb

class Next:
    def __init__(self):
        self.events = []

    def receive(self, event):
        self.events.append(event)

def absolute_time(ts):
    def _time():
        return ts
    return _time

# IP = "172.17.0.2"
# #logging.basicConfig(level=logging.DEBUG)
# class TestInputRethinkdb(unittest.TestCase):
#     def setUp(self):
#         adapter = RethinkdbAdapter(IP, timestamp_index="timestamp")
#         adapter.connect()

#         docs = [{"timestamp":1607904000+i, "line":"line of time {}".format(1607904000 + i)} for i in range(0, 3600*24, 1800)]
#         adapter.create_table_unique("log_20201214")
#         adapter.insert_bulk("log_20201214", docs)

#         docs = [{"timestamp":1607990400+i, "line":"line of time {}".format(1607990400 + i)} for i in range(0, 3600*24, 1800)]
#         adapter.create_table_unique("log_20201215")
#         adapter.insert_bulk("log_20201215", docs)

#         adapter.close()

#     def tearDown(self):
#         adapter = RethinkdbAdapter(IP, timestamp_index="timestamp")
#         adapter.connect()
#         adapter.delete_table("log_20201214")
#         adapter.delete_table("log_20201215")
#         adapter.close()

#     def test_init(self):
#         input_rethinkdb = InputRethinkdb(tag="log", 
#                                     window=3600, 
#                                     timestamp_index="timestamp", 
#                                     table_name_match="log_*", 
#                                     ip=IP)
 
#     def test_reload(self):

#         next_action = Next()

#         input_rethinkdb = InputRethinkdb(tag="log", 
#                                     window=3600, 
#                                     timestamp_index="timestamp", 
#                                     table_name_match="log_*", 
#                                     ip=IP,
#                                     reload_position=True)
#         input_rethinkdb.set_next(next_action)

#         input_rethinkdb.update(absolute_time(1608055200))# dec 15 18h00
#         input_rethinkdb.finish()

#         result = next_action.events[0].record, next_action.events[-1].record

#         expected = ({'line': 'line of time 1607904000', 'timestamp': 1607904000}, {'line': 'line of time 1608053400', 'timestamp': 1608053400})
#         self.assertEqual(result, expected)

#     def test_no_reload(self):

#         next_action = Next()

#         input_rethinkdb = InputRethinkdb(tag="log", 
#                                     window=3600, 
#                                     timestamp_index="timestamp", 
#                                     table_name_match="log_*", 
#                                     ip=IP,
#                                     reload_position=False)
#         input_rethinkdb.set_next(next_action)

#         input_rethinkdb.update(absolute_time(1608055200))# dec 15 18h00
#         input_rethinkdb.finish()

#         result = next_action.events
#         expected = []
#         self.assertEqual(result, expected)

#     def test_2_updates(self):

#         next_action = Next()

#         input_rethinkdb = InputRethinkdb(tag="log", 
#                                     window=3600, 
#                                     timestamp_index="timestamp", 
#                                     table_name_match="log_*", 
#                                     ip=IP,
#                                     reload_position=False)
#         input_rethinkdb.set_next(next_action)

#         input_rethinkdb.update(absolute_time(1608055200))# dec 15 18h00
#         # get the last windows
#         input_rethinkdb.update(absolute_time(1608055200+3600))# dec 15 19h00


#         tmp = next_action.events
#         result = tmp[0].record, tmp[1].record

#         expected = {'line': 'line of time 1608055200', 'timestamp': 1608055200}, {'line': 'line of time 1608057000', 'timestamp': 1608057000}
#         self.assertEqual(result, expected)

#     def test_3_updates(self):

#         next_action = Next()

#         input_rethinkdb = InputRethinkdb(tag="log", 
#                                     window=3600, 
#                                     timestamp_index="timestamp", 
#                                     table_name_match="log_*", 
#                                     ip=IP,
#                                     reload_position=False)
#         input_rethinkdb.set_next(next_action)

#         input_rethinkdb.update(absolute_time(1608055200))# dec 15 18h00
#         # get the last windows
#         input_rethinkdb.update(absolute_time(1608055200+3600))# dec 15 19h00
#         input_rethinkdb.update(absolute_time(1608055200+3600*2))# dec 15 20h00


#         tmp = next_action.events
#         result = tmp[-2].record, tmp[-1].record
        
#         expected = {'line': 'line of time 1608058800', 'timestamp': 1608058800}, {'line': 'line of time 1608060600', 'timestamp': 1608060600}
#         self.assertEqual(result, expected)

#     def test_reload_and_remove(self):

#         input_rethinkdb = InputRethinkdb(tag="log", 
#                                     window=3600, 
#                                     timestamp_index="timestamp", 
#                                     table_name_match="log_*", 
#                                     ip=IP,
#                                     reload_position=True,
#                                     remove=True)

#         input_rethinkdb.update(absolute_time(1608055200))# dec 15 18h00
#         input_rethinkdb.finish()

#         adapter = RethinkdbAdapter(IP, timestamp_index="timestamp")
#         adapter.connect()

#         # table should not exist !
#         result = adapter.list_tables()
#         #pprint(adapter.get_time_serie("log_20201214", "timestamp", 0, 1608055200)) # zero to dec 15 18h00
#         adapter.close()
#         expected = ["log_20201215"]
#         self.assertEqual(result, expected)

#     def test_no_reload_with_offset(self):

#         next_action = Next()

#         input_rethinkdb = InputRethinkdb(tag="log", 
#                                     window=3600, 
#                                     timestamp_index="timestamp", 
#                                     table_name_match="log_*", 
#                                     ip=IP,
#                                     reload_position=False,
#                                     offset=-3600)
#         input_rethinkdb.set_next(next_action)

#         input_rethinkdb.update(absolute_time(1608055200))# dec 15 18h00
#         input_rethinkdb.finish()

#         result = next_action.events
#         expected = []
#         self.assertEqual(result, expected)

#     def test_2_updates_with_offset(self):

#         next_action = Next()

#         input_rethinkdb = InputRethinkdb(tag="log", 
#                                     window=3600, 
#                                     timestamp_index="timestamp", 
#                                     table_name_match="log_*", 
#                                     ip=IP,
#                                     reload_position=False,
#                                     offset=-3600)
#         input_rethinkdb.set_next(next_action)

#         input_rethinkdb.update(absolute_time(1608055200))# dec 15 18h00 -> 17h
#         # get the last windows
#         input_rethinkdb.update(absolute_time(1608055200+3600))# dec 15 19h00 -> 18h


#         tmp = next_action.events
#         result = tmp[0].record, tmp[1].record

#         expected = {'line': 'line of time 1608051600', 'timestamp': 1608051600}, {'line': 'line of time 1608053400', 'timestamp': 1608053400}
#         self.assertEqual(result, expected)
