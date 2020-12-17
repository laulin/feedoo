from feedoo.rethinkdb_adapter import RethinkdbAdapter
import unittest
from pprint import pprint
from rethinkdb import r as Rethinkdb

# IP = "172.17.0.2"
# class TestRethinkdbAdapter(unittest.TestCase):
#     def tearDown(self):
#         conn = Rethinkdb.connect(IP, 28015)
#         Rethinkdb.db("test").table("first_table").delete().run(conn)
#         conn.close()
#         pass

#     def test_connection(self):
#         rethink = RethinkdbAdapter(IP)
#         rethink.connect()
#         rethink.close()

#     # def test_connection_bad_ip(self):
#     #     rethink = RethinkdbAdapter("10.11.12.13", wait_connection=1)
#     #     rethink.connect()
#     #     rethink.close()

#     def test_create_table(self):
#         rethink = RethinkdbAdapter(IP)
#         rethink.connect()
#         rethink.create_table_unique("first_table")
#         rethink.close()

#     def test_create_table_double(self):
#         rethink = RethinkdbAdapter(IP)
#         rethink.connect()
#         rethink.create_table_unique("first_table")
#         rethink.create_table_unique("first_table")
#         rethink.close()

#     def test_insert_bulk(self):
#         rethink = RethinkdbAdapter(IP)
#         rethink.connect()
#         rethink.create_table_unique("first_table")
#         rethink.insert_bulk("first_table", [{"name":"toto", "age":20}])
#         rethink.close()

#     def test_insert_bulk_bad_type(self):
#         # SQLITE allows that #fun
#         rethink = RethinkdbAdapter(IP)
#         rethink.connect()
#         rethink.create_table_unique("first_table")
#         result = rethink.insert_bulk("first_table", [{"name":20, "age":"toto"}])
#         rethink.close()

#     def test_get_time_serie(self):
#         rethink = RethinkdbAdapter(IP)
#         rethink.connect()
#         rethink.create_table_unique("first_table")
#         docs = [
#             {"timestamp":10, "name":"toto", "age":20},
#             {"timestamp":20, "name":"titi", "age":20},
#             {"timestamp":30, "name":"foo", "age":20},
#             {"timestamp":40, "name":"bar", "age":20},
#             {"timestamp":50, "name":"stuff", "age":20},
#             {"timestamp":60, "name":"dude", "age":20}
#         ]
#         rethink.insert_bulk("first_table", docs)

#         time_serie_docs = rethink.get_time_serie("first_table", "timestamp", 20, 50) # expect 20, 30, 40
#         rethink.close()
#         pprint(time_serie_docs)
#         expected = [
#             {'age': 20, 'name': 'titi', 'timestamp': 20},
#             {'age': 20, 'name': 'foo', 'timestamp': 30},
#             {'age': 20, 'name': 'bar', 'timestamp': 40},
#             {"timestamp":50, "name":"stuff", "age":20}
#             ]
#         self.assertEqual(time_serie_docs, expected)

#     def test_list_tables(self):
#         rethink = RethinkdbAdapter(IP)
#         rethink.connect()
#         rethink.create_table_unique("first_table")
#         result = rethink.list_tables()
#         rethink.close()

#         expected = ["first_table"]
#         self.assertEqual(result, expected)

#     def test_is_table_empty_true(self):
#         rethink = RethinkdbAdapter(IP)
#         rethink.connect()
#         rethink.create_table_unique("first_table")
#         result = rethink.is_table_empty("first_table")
#         rethink.close()

#         self.assertTrue(result)

#     def test_is_table_empty_false(self):
#         rethink = RethinkdbAdapter(IP)
#         rethink.connect()
#         rethink.create_table_unique("first_table")
#         rethink.insert_bulk("first_table", [{"name":"toto", "age":20}])
#         result = rethink.is_table_empty("first_table")
#         rethink.close()

#         self.assertFalse(result)

#     def test_get_min(self):
#         rethink = RethinkdbAdapter(IP)
#         rethink.connect()
#         rethink.create_table_unique("first_table")
#         docs = [
#             {"timestamp":10, "name":"toto", "age":20},
#             {"timestamp":20, "name":"titi", "age":20},
#             {"timestamp":30, "name":"foo", "age":20},
#             {"timestamp":40, "name":"bar", "age":20},
#             {"timestamp":50, "name":"stuff", "age":20},
#             {"timestamp":60, "name":"dude", "age":20}
#         ]
#         rethink.insert_bulk("first_table", docs)

#         result = rethink.get_min("first_table", "timestamp")
#         rethink.close()
#         expected = 10
#         self.assertEqual(result, expected)

#     def test_get_max(self):
#         rethink = RethinkdbAdapter(IP)
#         rethink.connect()
#         rethink.create_table_unique("first_table")
#         docs = [
#             {"timestamp":10, "name":"toto", "age":20},
#             {"timestamp":20, "name":"titi", "age":20},
#             {"timestamp":30, "name":"foo", "age":20},
#             {"timestamp":40, "name":"bar", "age":20},
#             {"timestamp":50, "name":"stuff", "age":20},
#             {"timestamp":60, "name":"dude", "age":20}
#         ]
#         rethink.insert_bulk("first_table", docs)

#         result = rethink.get_max("first_table", "timestamp")
#         rethink.close()
#         expected = 60
#         self.assertEqual(result, expected)

#     def test_delete_time_serie(self):
#         rethink = RethinkdbAdapter(IP)
#         rethink.connect()
#         rethink.create_table_unique("first_table")
#         docs = [
#             {"timestamp":10, "name":"toto", "age":20},
#             {"timestamp":20, "name":"titi", "age":20},
#             {"timestamp":30, "name":"foo", "age":20},
#             {"timestamp":40, "name":"bar", "age":20},
#             {"timestamp":50, "name":"stuff", "age":20},
#             {"timestamp":60, "name":"dude", "age":20}
#         ]
#         rethink.insert_bulk("first_table", docs)

#         rethink.delete_time_serie("first_table", "timestamp", 10, 60) # expect 20, 30, 40
#         result = rethink.is_table_empty("first_table")
#         rethink.close()
#         self.assertEqual(result, True)

