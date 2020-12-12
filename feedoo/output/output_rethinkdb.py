import time
from collections import defaultdict
import unittest
import logging

from rethinkdb import r as Rethinkdb
from chronyk import Chronyk

from feedoo.abstract_action import AbstractAction
from feedoo.event import Event
from feedoo.hash_storage import HashStorage

# push document to db

class OutputRethinkdb(AbstractAction):
    def __init__(self, match, time_key, table_template, buffer_size=1000, database="test", ip="localhost", port=None, wait_connection=30, timeout_flush=60, db_path=None):
        AbstractAction.__init__(self, match)
        self._time_key = time_key
        self._table_template = table_template
        self._buffer = HashStorage(db_path, timeout=timeout_flush)
        self._database = database
        self._ip = ip
        self._port = port
        self._buffer_size = buffer_size
        self._wait_connection = wait_connection
        self._log = logging.getLogger("ActionRethinkdb")

    def do(self, event):
        record = event.record
        timestamp = Chronyk(record[self._time_key])
        tablename = timestamp.timestring(self._table_template)
        tablename = tablename.format(**record)
        if tablename not in self._buffer:
            self._buffer[tablename] = list()

        buffer = self._buffer[tablename]
        buffer.append(record)
        self._buffer[tablename] = buffer

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

    def update(self, _time=time.time):
        for tablename in tuple(self._buffer.get_timeout(_time)):
            self._log.info("Flush (timeout) {}".format(tablename))
            self.flush_one(tablename)