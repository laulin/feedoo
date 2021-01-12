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

    def test_prod(self):
        parameters = {
        "time_key" : "timestamp",
        "filename" : DB_FILE,
        "table_template" : "sys_ram_%Y%m%d",
        "fields" :{
            "eth0_rx_packets": "INTEGER",
            "eth0_rx_errors": "INTEGER",
            "eth0_rx_bytes": "INTEGER",
            "eth0_tx_packets": "INTEGER",
            "eth0_tx_errors": "INTEGER",
            "eth0_tx_bytes": "INTEGER",
            "source": "TEXT",
            "timestamp": "INTEGER"
        },
        "buffer_size" : 10,
        "match" : "sys.netif",
        "db_path": "/tmp/cache.db"
        }

        output_sqlite = OutputSqlite(**parameters)
        data = [{'source': 'jarvis-2', 'tag': 'sys.ram', 'timestamp': 1609928073, 'Mem_used': 1732584, 'Mem_free': 2186188, 'Swap_total': 102396, 'Swap_used': 2048, 'Swap_free': 100348, 'Mem_total': 3918772}, 
        {'source': 'jarvis-2', 'tag': 'sys.ram', 'timestamp': 1609928074, 'Mem_used': 1732592, 'Mem_free': 2186180, 'Swap_total': 102396, 'Swap_used': 2048, 'Swap_free': 100348, 'Mem_total': 3918772}, 
        {'source': 'jarvis-2', 'tag': 'sys.ram', 'timestamp': 1609928075, 'Mem_used': 1732584, 'Mem_free': 2186188, 'Swap_total': 102396, 'Swap_used': 2048, 'Swap_free': 100348, 'Mem_total': 3918772}, 
        {'source': 'jarvis-2', 'tag': 'sys.ram', 'timestamp': 1609928076, 'Mem_used': 1732616, 'Mem_free': 2186156, 'Swap_total': 102396, 'Swap_used': 2048, 'Swap_free': 100348, 'Mem_total': 3918772}, 
        {'source': 'jarvis-2', 'tag': 'sys.ram', 'timestamp': 1609928078, 'Mem_used': 1732836, 'Mem_free': 2185936, 'Swap_total': 102396, 'Swap_used': 2048, 'Swap_free': 100348, 'Mem_total': 3918772}, 
        {'source': 'jarvis-2', 'timestamp': 1609928078, 'tag': 'sys.ram', 'Mem_used': 1733072, 'Mem_free': 2185700, 'Swap_total': 102396, 'Swap_used': 2048, 'Swap_free': 100348, 'Mem_total': 3918772}, 
        {'source': 'jarvis-2', 'tag': 'sys.ram', 'timestamp': 1609928079, 'Mem_used': 1733104, 'Mem_free': 2185668, 'Swap_total': 102396, 'Swap_used': 2048, 'Swap_free': 100348, 'Mem_total': 3918772}, 
        {'source': 'jarvis-2', 'tag': 'sys.ram', 'timestamp': 1609928080, 'Mem_used': 1733104, 'Mem_free': 2185668, 'Swap_total': 102396, 'Swap_used': 2048, 'Swap_free': 100348, 'Mem_total': 3918772}, 
        {'source': 'jarvis-2', 'tag': 'sys.ram', 'timestamp': 1609928081, 'Mem_used': 1733088, 'Mem_free': 2185684, 'Swap_total': 102396, 'Swap_used': 2048, 'Swap_free': 100348, 'Mem_total': 3918772}, 
        {'source': 'jarvis-2', 'tag': 'sys.ram', 'timestamp': 1609928082, 'Mem_used': 1733072, 'Mem_free': 2185700, 'Swap_total': 102396, 'Swap_used': 2048, 'Swap_free': 100348, 'Mem_total': 3918772}]
        
        for d in data:
            event = Event("sys.netif", 1608026350, d)
            output_sqlite.do(event)

        output_sqlite.finish()

        # read back the db
        db = SqliteAdapter(DB_FILE, parameters["fields"])
        db.connect()
        result = db.get_time_serie("sys_ram_20210106", "timestamp", 1609928072, 1609928083)
        #print(db.list_tables())
        db.close()
        print(result)

        # self.assertEqual(len(result), 1)
