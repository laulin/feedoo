from feedoo.sqlite_adapter import SqliteAdapter
import unittest
from pprint import pprint


class TestSqliteAdapter(unittest.TestCase):
    def test_create_table(self):
        sa = SqliteAdapter(":memory:", {"name":"TEXT", "age":"INTEGER"})
        sa.connect()
        sa.create_table_unique("first_table")
        sa.close()

    def test_create_table_double(self):
        sa = SqliteAdapter(":memory:", {"name":"TEXT", "age":"INTEGER"})
        sa.connect()
        sa.create_table_unique("first_table")
        sa.create_table_unique("first_table")
        sa.close()

    def test_insert_bulk(self):
        sa = SqliteAdapter(":memory:", {"name":"TEXT", "age":"INTEGER"})
        sa.connect()
        sa.create_table_unique("first_table")
        sa.insert_bulk("first_table", [{"name":"toto", "age":20}])
        sa.close()

    def test_insert_bulk_bad_type(self):
        # SQLITE allows that #fun
        sa = SqliteAdapter("/tmp/db/example.db", {"name":"TEXT", "age":"INTEGER"})
        sa.connect()
        sa.create_table_unique("first_table")
        result = sa.insert_bulk("first_table", [{"name":20, "age":"toto"}])
        sa.close()

    def test_get_time_serie(self):
        sa = SqliteAdapter(":memory:", {"timestamp":"INTEGER", "name":"TEXT", "age":"INTEGER"})
        sa.connect()
        sa.create_table_unique("first_table")
        docs = [
            {"timestamp":10, "name":"toto", "age":20},
            {"timestamp":20, "name":"titi", "age":20},
            {"timestamp":30, "name":"foo", "age":20},
            {"timestamp":40, "name":"bar", "age":20},
            {"timestamp":50, "name":"stuff", "age":20},
            {"timestamp":60, "name":"dude", "age":20}
        ]
        sa.insert_bulk("first_table", docs)

        time_serie_docs = sa.get_time_serie("first_table", "timestamp", 20, 50) # expect 20, 30, 40
        sa.close()
        pprint(time_serie_docs)
        expected = [
            {'age': 20, 'name': 'titi', 'timestamp': 20},
            {'age': 20, 'name': 'foo', 'timestamp': 30},
            {'age': 20, 'name': 'bar', 'timestamp': 40}
            ]

        self.assertEqual(time_serie_docs, expected)
