from feedoo.input.input_sqlite import InputSqlite
from feedoo.sqlite_adapter import SqliteAdapter
import unittest
import os
import logging
from pprint import pprint

class Next:
    def __init__(self):
        self.events = []

    def receive(self, event):
        self.events.append(event)

def absolute_time(ts):
    def _time():
        return ts
    return _time

FIELDS = {"timestamp":"INTEGER", "line":"TEXT"}
FILENAME = "/tmp/test.db"
#logging.basicConfig(level=logging.DEBUG)
class TestInputSqlite(unittest.TestCase):
    def setUp(self):
        sqlite_adapter = SqliteAdapter(FILENAME, FIELDS)
        sqlite_adapter.connect()

        docs = [{"timestamp":1607904000+i, "line":"line of time {}".format(1607904000 + i)} for i in range(0, 3600*24, 1800)]
        sqlite_adapter.create_table_unique("log_20201214")
        sqlite_adapter.insert_bulk("log_20201214", docs)

        docs = [{"timestamp":1607990400+i, "line":"line of time {}".format(1607990400 + i)} for i in range(0, 3600*24, 1800)]
        sqlite_adapter.create_table_unique("log_20201215")
        sqlite_adapter.insert_bulk("log_20201215", docs)

        sqlite_adapter.close()

    def tearDown(self):
        os.remove(FILENAME)


    def test_init(self):
        input_sqlite = InputSqlite(tag="log", 
                                    window=3600, 
                                    time_key="timestamp", 
                                    table_name_match="log_*", 
                                    filename=FILENAME, 
                                    fields=FIELDS)
 
    def test_reload(self):

        next_action = Next()

        input_sqlite = InputSqlite(tag="log", 
                                    window=3600, 
                                    time_key="timestamp", 
                                    table_name_match="log_*", 
                                    filename=FILENAME, 
                                    fields=FIELDS,
                                    reload_position=True)
        input_sqlite.set_next(next_action)

        input_sqlite.update(absolute_time(1608055200))# dec 15 18h00
        input_sqlite.finish()

        result = next_action.events[0].record, next_action.events[-1].record

        expected = ({'line': 'line of time 1607904000', 'timestamp': 1607904000}, {'line': 'line of time 1608053400', 'timestamp': 1608053400})
        self.assertEqual(result, expected)

    def test_no_reload(self):

        next_action = Next()

        input_sqlite = InputSqlite(tag="log", 
                                    window=3600, 
                                    time_key="timestamp", 
                                    table_name_match="log_*", 
                                    filename=FILENAME, 
                                    fields=FIELDS,
                                    reload_position=False)
        input_sqlite.set_next(next_action)

        input_sqlite.update(absolute_time(1608055200))# dec 15 18h00
        input_sqlite.finish()

        result = next_action.events
        expected = []
        self.assertEqual(result, expected)

    def test_2_updates(self):

        next_action = Next()

        input_sqlite = InputSqlite(tag="log", 
                                    window=3600, 
                                    time_key="timestamp", 
                                    table_name_match="log_*", 
                                    filename=FILENAME, 
                                    fields=FIELDS,
                                    reload_position=False)
        input_sqlite.set_next(next_action)

        input_sqlite.update(absolute_time(1608055200))# dec 15 18h00
        # get the last windows
        input_sqlite.update(absolute_time(1608055200+3600))# dec 15 19h00


        tmp = next_action.events
        result = tmp[0].record, tmp[1].record

        expected = {'line': 'line of time 1608055200', 'timestamp': 1608055200}, {'line': 'line of time 1608057000', 'timestamp': 1608057000}
        self.assertEqual(result, expected)

    def test_3_updates(self):

        next_action = Next()

        input_sqlite = InputSqlite(tag="log", 
                                    window=3600, 
                                    time_key="timestamp", 
                                    table_name_match="log_*", 
                                    filename=FILENAME, 
                                    fields=FIELDS,
                                    reload_position=False)
        input_sqlite.set_next(next_action)

        input_sqlite.update(absolute_time(1608055200))# dec 15 18h00
        # get the last windows
        input_sqlite.update(absolute_time(1608055200+3600))# dec 15 19h00
        input_sqlite.update(absolute_time(1608055200+3600*2))# dec 15 20h00


        tmp = next_action.events
        result = tmp[-2].record, tmp[-1].record
        
        expected = {'line': 'line of time 1608058800', 'timestamp': 1608058800}, {'line': 'line of time 1608060600', 'timestamp': 1608060600}
        self.assertEqual(result, expected)

    def test_reload_and_remove(self):

        input_sqlite = InputSqlite(tag="log", 
                                    window=3600, 
                                    time_key="timestamp", 
                                    table_name_match="log_*", 
                                    filename=FILENAME, 
                                    fields=FIELDS,
                                    reload_position=True,
                                    remove=True)

        input_sqlite.update(absolute_time(1608055200))# dec 15 18h00
        input_sqlite.finish()

        sqlite_adapter = SqliteAdapter(FILENAME, FIELDS)
        sqlite_adapter.connect()

        # table should not exist !
        result = sqlite_adapter.list_tables()
        #pprint(sqlite_adapter.get_time_serie("log_20201214", "timestamp", 0, 1608055200)) # zero to dec 15 18h00
        sqlite_adapter.close()
        expected = ["log_20201215"]
        self.assertEqual(result, expected)

    def test_no_reload_with_offset(self):

        next_action = Next()

        input_sqlite = InputSqlite(tag="log", 
                                    window=3600, 
                                    time_key="timestamp", 
                                    table_name_match="log_*", 
                                    filename=FILENAME, 
                                    fields=FIELDS,
                                    reload_position=False,
                                    offset=-3600)
        input_sqlite.set_next(next_action)

        input_sqlite.update(absolute_time(1608055200))# dec 15 18h00
        input_sqlite.finish()

        result = next_action.events
        expected = []
        self.assertEqual(result, expected)

    def test_2_updates_with_offset(self):

        next_action = Next()

        input_sqlite = InputSqlite(tag="log", 
                                    window=3600, 
                                    time_key="timestamp", 
                                    table_name_match="log_*", 
                                    filename=FILENAME, 
                                    fields=FIELDS,
                                    reload_position=False,
                                    offset=-3600)
        input_sqlite.set_next(next_action)

        input_sqlite.update(absolute_time(1608055200))# dec 15 18h00 -> 17h
        # get the last windows
        input_sqlite.update(absolute_time(1608055200+3600))# dec 15 19h00 -> 18h


        tmp = next_action.events
        result = tmp[0].record, tmp[1].record

        expected = {'line': 'line of time 1608051600', 'timestamp': 1608051600}, {'line': 'line of time 1608053400', 'timestamp': 1608053400}
        self.assertEqual(result, expected)



        

