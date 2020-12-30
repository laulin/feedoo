from collections.abc import MutableMapping
from collections import OrderedDict
import json
from time import time
import sqlite3

"""
Store key:str, timestamp:int, value:bytes in table (default : HashStore)
""" 


class HashStorage(MutableMapping):
    """A dictionary that store any change and can be loaded/stored with a timeout management"""

    def __init__(self, path:str=None, timeout:int=60):
        self._data = None  # key:value
        self._timeout = timeout 
        self._key_timeout = None  # key:timeout, OrderedDict
        self._path = path

    def _late_init(self):
        # post pone dict load to allow low right to be applied
        if self._data is None:
            if self._path is not None:
                try:
                    with open(self._path) as f:
                        raw_data = f.read()
                        data = json.loads(raw_data)
                        self._data = data["data"]
                        self._key_timeout = OrderedDict(data["key_timeout"])
                except Exception as e:
                    # print(e)
                    self._data = dict()
                    self._key_timeout = OrderedDict()
            else:
                self._data = dict()
                self._key_timeout = OrderedDict()

    def dump(self):
        self._late_init()
        #print("dump !!!")
        if self._path is not None:
            with open(self._path, "w") as f:
                data = {"data":self._data, "key_timeout":self._key_timeout}
                raw_data = json.dumps(data, indent=4)
                f.write(raw_data)


    def get_timeout(self, _time=time):
        self._late_init()
        timestamp = int(_time()) - self._timeout
        
        output = []
        for k, t in self._key_timeout.items():
            if t < timestamp:
                output.append(k)
            else:
                return output

        return output
            
    def __getitem__(self, key):
        self._late_init()
        return self._data[key]


    def __setitem__(self, key, value):
        self._late_init()
        timestamp = int(time())
        
        self._data[key] = value

        if key in self._key_timeout:
            del self._key_timeout[key]
        self._key_timeout[key] = timestamp

    def __delitem__(self, key):
        self._late_init()
        del self._data[key]
        del self._key_timeout[key]

    def __iter__(self):
        self._late_init()
        return self._data.keys() 
    
    def __len__(self):
        self._late_init()
        return len(self._data)

    def __repr__(self):
        self._late_init()
        output = "key;timestamp;value\n"

        tmp = ["{};{};{}".format(k,self._data[k], self._key_timeout[k]) for k in self._data]

        return output + "\n".join(tmp)

    def keys(self):
        self._late_init()
        return self._data.keys()

    def values(self):
        self._late_init()
        return self._data.values()

    def items(self):
        self._late_init()
        return self._data.items()
