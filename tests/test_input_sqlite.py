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
logging.basicConfig(level=logging.DEBUG)
class TestInputSqlite(unittest.TestCase):
    def setUp(self):
        sqlite_adapter = SqliteAdapter(FILENAME, FIELDS)
        sqlite_adapter.connect()

        docs = [{"timestamp":1607904000+i, "line":"line of time {}".format(1607904000 + i)} for i in range(0, 3600*24, 30)]
        #pprint(docs)
        sqlite_adapter.create_table_unique("log_20201214")
        sqlite_adapter.insert_bulk("log_20201214", docs)

        docs = [{"timestamp":1607990400+i, "line":"line of time {}".format(1607990400 + i)} for i in range(0, 3600*24, 30)]
        sqlite_adapter.create_table_unique("log_20201215")
        sqlite_adapter.insert_bulk("log_20201215", docs)

        sqlite_adapter.close()

    def tearDown(self):
        os.remove(FILENAME)


    def test_init(self):
        input_sqlite = InputSqlite(tag="log", 
                                    windows=60, 
                                    time_key="timestamp", 
                                    table_name_match="log_*", 
                                    filename=FILENAME, 
                                    fields=FIELDS)
 
    def test_reload(self):

        next_action = Next()

        input_sqlite = InputSqlite(tag="log", 
                                    windows=60, 
                                    time_key="timestamp", 
                                    table_name_match="log_*", 
                                    filename=FILENAME, 
                                    fields=FIELDS,
                                    reload_position=True)
        input_sqlite.set_next(next_action)

        input_sqlite.update(absolute_time(1608055200))# dec 15 18h00
        input_sqlite.finish()

        result = next_action.events[0].record, next_action.events[-1].record
        expected = ({'line': 'line of time 1607904000', 'timestamp': 1607904000}, {'line': 'line of time 1608055170', 'timestamp': 1608055170})
        self.assertEqual(result, expected)

    def test_no_reload(self):

        next_action = Next()

        input_sqlite = InputSqlite(tag="log", 
                                    windows=60, 
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
                                    windows=60, 
                                    time_key="timestamp", 
                                    table_name_match="log_*", 
                                    filename=FILENAME, 
                                    fields=FIELDS,
                                    reload_position=False)
        input_sqlite.set_next(next_action)

        input_sqlite.update(absolute_time(1608055200))# dec 15 18h00
        # get the last windows
        input_sqlite.update(absolute_time(1608055200+60))# dec 15 18h01


        tmp = next_action.events
        result = tmp[0].record, tmp[1].record
        expected = {'line': 'line of time 1608055200', 'timestamp': 1608055200}, {'line': 'line of time 1608055230', 'timestamp': 1608055230}
        self.assertEqual(result, expected)

    def test_3_updates(self):

        next_action = Next()

        input_sqlite = InputSqlite(tag="log", 
                                    windows=60, 
                                    time_key="timestamp", 
                                    table_name_match="log_*", 
                                    filename=FILENAME, 
                                    fields=FIELDS,
                                    reload_position=False)
        input_sqlite.set_next(next_action)

        input_sqlite.update(absolute_time(1608055200))# dec 15 18h00
        # get the last windows
        input_sqlite.update(absolute_time(1608055200+60))# dec 15 18h01
        input_sqlite.update(absolute_time(1608055200+120))# dec 15 18h02


        tmp = next_action.events
        result = tmp[-2].record, tmp[-1].record
        expected = {'line': 'line of time 1608055260', 'timestamp': 1608055260}, {'line': 'line of time 1608055290', 'timestamp': 1608055290}
        self.assertEqual(result, expected)



        

