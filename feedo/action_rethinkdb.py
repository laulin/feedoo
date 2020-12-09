from rethinkdb import r as Rethinkdb
from chronyk import Chronyk
import time
from collections import defaultdict
from abstract_action import AbstractAction
from event import Event
import unittest
import logging
from hash_storage import HashStorage
from time import time

# push document to db

class ActionRethinkdb(AbstractAction):
    def __init__(self, match, time_key, table_template, buffer_size=1000, database="test", ip="localhost", port=None, wait_connection=30, timeout_flush=60):
        AbstractAction.__init__(self, match)
        self._time_key = time_key
        self._table_template = table_template
        self._buffer = HashStorage(timeout=timeout_flush)
        self._database = database
        self._ip = ip
        self._port = port
        self._buffer_size = buffer_size
        self._wait_connection = wait_connection
        self._log = logging.getLogger("ActionRethinkdb")

    def do(self, event):
        record = event.record
        time = Chronyk(record[self._time_key])
        tablename = time.timestring(self._table_template)
        tablename = tablename.format(**record)
        if tablename not in self._buffer:
            self._buffer[tablename] = list()

        self._buffer[tablename].append(record)

        if len(self._buffer[tablename]) > self._buffer_size:
            self.flush_one(tablename)

        return event

    def rethinkdb_waiting_connecton(self):
        """
        Wait for the database to be up and return connection
        """
        counter = self._wait_connection

        while True:
            try:
                connection = Rethinkdb.connect(self._ip, self._port)
                return connection
            except Exception as e:
                time.sleep(1)
                counter = counter -1

                if counter <= 0:
                    self._log.warning("Can't establish connection on {}:{}".format(self._ip, self._port))
                    raise e 

    def finish(self):
        self._log.debug("finish")

        for k in tuple(self._buffer.keys()):
            self._log.info("Flush (finish) {}".format(k))
            self.flush_one(k)

    def flush_one(self, tablename):
        self._log.info("flush "+tablename)
        try:
            connection = self.rethinkdb_waiting_connecton()
            tables = Rethinkdb.db(self._database).table_list().run(connection)

            if tablename not in tables:
                Rethinkdb.db(self._database).table_create(tablename).run(connection)
                self._log.info("create table "+tablename)
            values = self._buffer[tablename]
            
            Rethinkdb.table(tablename).index_wait().run(connection)
            Rethinkdb.table(tablename).insert(values).run(connection)
        except Exception as e:
            self._log.error("Can't insert data to {}:{}[{}][{}] ({})".format(self._ip, self._port, self._database, tablename, e))

        del self._buffer[tablename]

    def update(self, _time=time):
        for tablename in tuple(self._buffer.get_timeout(_time)):
            self._log.info("Flush (timeout) {}".format(tablename))
            self.flush_one(tablename)


# # Enable those tests only if a rethinkDB is up
# IP = "172.17.0.1"
# class TestActionRethinkdb(unittest.TestCase):
#     def test_1(self):
#         action = ActionRethinkdb("*", "timestamp", "sys-%Y%m%d", ip=IP)
#         event = Event("mytag", 123456789, {"timestamp":1603373121, "data":"aaaaaa"})
#         action.do(event)
#         action.finish()

#     def test_2(self):
#         action = ActionRethinkdb("*", "timestamp", "sys-%Y%m%d", ip=IP)
#         event_1 = Event("mytag", 1603373122, {"timestamp":1603373122, "data":"BBBB"})
#         action.do(event_1)
#         event_2 = Event("mytag", 1603373123,{"timestamp":1603373123, "data":"ccccc"})
#         action.do(event_2)
#         action.finish()

#     def test_force_flush(self):
#         action = ActionRethinkdb("*", "timestamp", "sys-%Y%m%d", buffer_size=1, ip=IP)
#         event_1 = Event("mytag", 1603373122, {"timestamp":1603373122, "data":"BBBB"})
#         action.do(event_1)
#         event_2 = Event("mytag", 1603373123,{"timestamp":1603373123, "data":"ccccc"})
#         action.do(event_2)

#     def test_timeout_update(self):
#         action = ActionRethinkdb("*", "timestamp", "sys-%Y%m%d", buffer_size=100, ip=IP)
#         event_1 = Event("mytag", 1603373122, {"timestamp":1603373122, "data":"BBBB"})
#         action.do(event_1)
#         event_2 = Event("mytag", 1603373123,{"timestamp":1603373123, "data":"ccccc"})
#         action.do(event_2)
#         def my_time():
#             return time() + 3600
#         action.update(my_time)








