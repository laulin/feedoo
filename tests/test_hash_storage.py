import unittest
from time import time
from feedoo.hash_storage import HashStorage
from feedoo.time_frame import TimeFrame
import os

DB_PATH = "/tmp/db.bin"
class TestHashStorage(unittest.TestCase):
    def setUp(self):
        try:
            os.remove(DB_PATH)
        except:
            pass

    def test_init(self):
        storage = HashStorage(DB_PATH)

    def test_double_init(self):
        storage = HashStorage(DB_PATH)
        storage2 = HashStorage(DB_PATH)

    def test_set(self):
        storage = HashStorage(DB_PATH)
        storage["x"] = "y"

    def test_double_set(self):
        storage = HashStorage(DB_PATH)
        storage["x"] = "y"
        storage["x"] = "z"

    def test_get(self):
        storage = HashStorage(DB_PATH)
        storage["x"] = "y"
        result = storage["x"]

        self.assertEqual(result, "y")

    def test_in(self):
        storage = HashStorage(DB_PATH)
        storage["x"] = "y"
        result = "x" in storage

        self.assertTrue(result)

    def test_in(self):
        storage = HashStorage(DB_PATH)
        storage["x"] = "y"
        result = "y" in storage

        self.assertFalse(result)

    def test_get_2(self):
        storage = HashStorage(DB_PATH)
        storage["x"] = "z"
        storage["x"] = "y"
        result = storage["x"]

        self.assertEqual(result, "y")

    def test_len(self):
        storage = HashStorage(DB_PATH)
        storage["x"] = "y"
        storage["y"] = "z"
        result = len(storage)

        self.assertEqual(result, 2)

    def test_no_timeout(self):
        storage = HashStorage()
        storage["key"] = "x"
        result = list(storage.get_timeout())

        self.assertEqual(len(result), 0)

    def test_timeout(self):
        storage = HashStorage()
        storage["key"] = "x"

        def mytime():
            t =  time() + 3600
            return t

        result = list(storage.get_timeout(mytime))

        self.assertEqual(result, ["key"])

    def test_get_time_frame(self):
        storage = HashStorage(DB_PATH)
        storage["x"] = TimeFrame(60)
        t = storage["x"]
        t.add_event("event")
        storage["x"] = t

        result = len(storage["x"])

        self.assertEqual(result, 1)

    def test_keys(self):
        storage = HashStorage(DB_PATH)
        storage["x"] = 1
        storage["y"] = 2
        result = list(storage.keys())
        expected = ["x", "y"]

        self.assertEqual(result, expected)

    def test_values(self):
        storage = HashStorage(DB_PATH)
        storage["x"] = 1
        storage["y"] = 2
        result = list(storage.values())
        expected = [1,2]

        self.assertEqual(result, expected)

    def test_items(self):
        storage = HashStorage(DB_PATH)
        storage["x"] = 1
        storage["y"] = 2
        result = list(storage.items())
        expected = [("x", 1),("y", 2)]

        self.assertEqual(result, expected)