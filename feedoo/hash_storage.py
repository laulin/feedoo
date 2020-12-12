from collections.abc import MutableMapping
import json
from time import time
import sqlite3
import pickle

"""
Store key:str, timestamp:int, value:bytes in table (default : HashStore)
""" 


class HashStorage(MutableMapping):
    """A dictionary that store any change and can be loaded/stored with a timeout management"""

    def __init__(self, path=None, timeout=60, table_name="HashStore"):
        if not path:
            path = ":memory:"

        self._table_name = table_name
        self._connection = sqlite3.connect(path)
        self._create_table()
        self._timeout = timeout

    def _create_table(self):
        cursor = self._connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS {} (key BLOB UNIQUE, timestamp INTEGER, value BLOB);".format(self._table_name))
        self._connection.commit()

    def get_timeout(self, _time=time):
        timestamp = int(_time()) - self._timeout
        
        cursor = self._connection.cursor()
        cursor.execute('SELECT key FROM {} WHERE timestamp < ?'.format(self._table_name), (timestamp,))
        row = cursor.fetchall()

        return map(lambda x : pickle.loads(x[0]), row)
            
    def __getitem__(self, key):
        blob_key = pickle.dumps(key)

        cursor = self._connection.cursor()
        cursor.execute('SELECT value FROM {} WHERE key = ?'.format(self._table_name), (blob_key,))
        row = cursor.fetchone()
        if row is None:
            raise KeyError(key)
        
        return pickle.loads(row[0])

    def __setitem__(self, key, value):
        timestamp = int(time())
        blop_value = pickle.dumps(value)
        blob_key = pickle.dumps(key)
        fields = (blob_key, timestamp, blop_value)
        cursor = self._connection.cursor()
        cursor.execute('''DELETE FROM {} WHERE key = ?'''.format(self._table_name), (blob_key,))
        cursor.execute('''INSERT INTO {}(key, timestamp, value) VALUES(?, ?, ?)'''.format(self._table_name), fields)

        self._connection.commit()

    def __delitem__(self, key):
        blob_key = pickle.dumps(key)
        cursor = self._connection.cursor()
        cursor.execute('''DELETE FROM {} WHERE key = ?'''.format(self._table_name), (blob_key,))

        self._connection.commit()

    def __iter__(self):
        cursor = self._connection.cursor()
        cursor.execute('SELECT key FROM {}'.format(self._table_name))
        rows = cursor.fetchall()

        return map(lambda x : pickle.loads(x[0]), rows)
    
    def __len__(self):
        cursor = self._connection.cursor()
        cursor.execute('SELECT count(value) FROM {}'.format(self._table_name))
        row = cursor.fetchone()
        return row[0]

    def __repr__(self):
        output = "key;timestamp;value\n"
        cursor = self._connection.cursor()
        cursor.execute('SELECT * FROM {}'.format(self._table_name))
        rows = cursor.fetchall()

        tmp = ["{};{};{}".format(pickle.loads(k),t,pickle.loads(v)) for k,t,v in rows]

        return output + "\n".join(tmp)

    def keys(self):
        cursor = self._connection.cursor()
        cursor.execute('SELECT key FROM {}'.format(self._table_name))
        rows = cursor.fetchall()

        return map(lambda x : pickle.loads(x[0]), rows)

    def values(self):
        cursor = self._connection.cursor()
        cursor.execute('SELECT value FROM {}'.format(self._table_name))
        rows = cursor.fetchall()

        return map(lambda x : pickle.loads(x[0]), rows)

    def items(self):
        cursor = self._connection.cursor()
        cursor.execute('SELECT key,value FROM {}'.format(self._table_name))
        rows = cursor.fetchall()

        return map(lambda x : (pickle.loads(x[0]), pickle.loads(x[1])), rows)
