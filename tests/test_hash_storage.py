import unittest
from time import time
from feedo.hash_storage import HashStorage

class TestHashStorage(unittest.TestCase):
    def test_no_timeout(self):
        storage = HashStorage()
        storage["key"] = "x"
        result = list(storage.get_timeout())

        self.assertEqual(len(result), 0)

    def test_timeout(self):
        storage = HashStorage()
        storage["key"] = "x"
        def mytime():
            return time() + 3600
        result = list(storage.get_timeout(mytime))

        self.assertEqual(result, ["key"])