from feedoo.output.output_sqlite import OutputSqlite
from feedoo.sqlite_adapter import SqliteAdapter
from feedoo.event import Event
import unittest
import time
import os

def my_time(dt):
    def t():
        return time.time() + dt
    return t

FIELDS = {"timestamp":"INTEGER", "name":"TEXT", "age":"INTEGER"}
DB_FILE = "/tmp/test.db"
class TestOutputSqlite(unittest.TestCase):
    def tearDown(self):
        
        try:
            os.remove(DB_FILE)
        except:
            pass

    def test_init(self):
        output_sqlite = OutputSqlite("*", "timestamp", "table_%Y%m%d", DB_FILE, FIELDS)

    def test_do(self):
        output_sqlite = OutputSqlite("*", "timestamp", "table_%Y%m%d", DB_FILE, FIELDS, buffer_size=1)
        event = Event("log", 1608026350, {"timestamp":1608026350, "name":"toto", "age":20}) # 1608026350 = Tue, 15 Dec 2020 09:59:10 GMT
        output_sqlite.do(event)
        event = Event("log", 1608026351, {"timestamp":1608026351, "name":"titi", "age":21}) # dump because buffer is full
        output_sqlite.do(event)

        # read back the db
        db = SqliteAdapter(DB_FILE, FIELDS)
        db.connect()
        result = db.get_time_serie("table_20201215", "timestamp", 1608026349, 1608026359)
        db.close()

        self.assertEqual(len(result), 2)

    def test_update(self):
        output_sqlite = OutputSqlite("*", "timestamp", "table_%Y%m%d", DB_FILE, FIELDS, buffer_size=1)
        event = Event("log", 1608026350, {"timestamp":1608026350, "name":"toto", "age":20}) # 1608026350 = Tue, 15 Dec 2020 09:59:10 GMT
        output_sqlite.do(event)

        output_sqlite.update(my_time(120))

        # read back the db
        db = SqliteAdapter(DB_FILE, FIELDS)
        db.connect()
        result = db.get_time_serie("table_20201215", "timestamp", 1608026349, 1608026359)
        db.close()

        self.assertEqual(len(result), 1)

    def test_finish(self):
        output_sqlite = OutputSqlite("*", "timestamp", "table_%Y%m%d", DB_FILE, FIELDS, buffer_size=1)
        event = Event("log", 1608026350, {"timestamp":1608026350, "name":"toto", "age":20}) # 1608026350 = Tue, 15 Dec 2020 09:59:10 GMT
        output_sqlite.do(event)

        output_sqlite.finish()

        # read back the db
        db = SqliteAdapter(DB_FILE, FIELDS)
        db.connect()
        result = db.get_time_serie("table_20201215", "timestamp", 1608026349, 1608026359)
        db.close()

        self.assertEqual(len(result), 1)
