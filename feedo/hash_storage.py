from collections.abc import MutableMapping
import json
import unittest
from time import time


class HashStorage(MutableMapping):
    """A dictionary that store any change and can be loaded/stored with a timeout management"""

    def __init__(self, path=None, timeout=60):
        self._changed = False
        self._store = dict()
        self._last_update = dict()
        self._path = path
        self._timeout = timeout

    def load(self, ignore_missing=True):
        if self._path is not None:
            self._changed = False
            
            try:
                with open(self._path) as f:
                    raw_data = f.read()
                    data = json.loads(raw_data)
                    self._store = data["store"]
                    self._last_update = data["last_update"]
            except IOError as e: 
                # ignore is file is not available
                if not ignore_missing:
                    raise e

    def store(self):
        if self._path is not None and self._changed:
            self._changed = False
            
            with open(self._path, "w") as f:
                data = dict()
                data["store"] = self._store
                data["last_update"] = self._last_update
                raw_data = json.dumps(data, sort_keys=True, indent=4)
                f.write(raw_data)

    def get_timeout(self, _time=time):
        current_time = _time()
        reference_time = current_time - self._timeout
        tmp = filter(lambda t: t[1] < reference_time, self._last_update.items()) # get outdated key, value by value (time)
        return map(lambda x: x[0], tmp) # return outdated keys
            
    def is_changed(self):
        return self._changed

    def __getitem__(self, key):
        return self._store[key]

    def __setitem__(self, key, value):
        if key not in self._store or self._store[key] != value:
            self._changed = True
        self._store[key] = value
        self._last_update[key] = time()

    def __delitem__(self, key):
        del self._store[key]
        del self._last_update[key]

    def __iter__(self):
        return iter(self._store)
    
    def __len__(self):
        return len(self._store)

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