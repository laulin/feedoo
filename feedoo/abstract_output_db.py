from feedoo.abstract_action import AbstractAction
from feedoo.hash_storage import HashStorage
from chronyk import Chronyk
import time

class AbstractOutputDB(AbstractAction):
    def __init__(self, match, time_key, table_template, buffer_size=1000, timeout_flush=60, db_path=None):
        AbstractAction.__init__(self, match)
        self._database_adapter = None
        self._time_key = time_key
        self._table_template = table_template
        self._buffer = HashStorage(db_path, timeout=timeout_flush)
        self._buffer_size = buffer_size

    def _create_table_name(self, event):
        timestamp = Chronyk(event.record[self._time_key])
        tablename = timestamp.timestring(self._table_template)
        tablename = tablename.format(**event.record)

        return tablename

    def do(self, event, _time=time.time):
        tablename = self._create_table_name(event)
        if tablename not in self._buffer:
            self._buffer[tablename] = list()

        
        buffer = self._buffer[tablename]
        buffer.append(event.record)
        self._buffer[tablename] = buffer

        if len(self._buffer[tablename]) > self._buffer_size:
            self.flush_one(tablename)

        return event

    def flush_one(self, tablename):
        self._log.info("flush "+tablename)
        try:
            if not self._database_adapter.is_connected():
                self._database_adapter.connect()

            self._database_adapter.create_table_unique(tablename)
            documents = self._buffer[tablename]
            self._database_adapter.insert_bulk(tablename, documents)
            
        except Exception as e:
            self._log.error("Can't insert data ({})".format(repr(e)))

        del self._buffer[tablename]

    def update(self, _time=time.time):
        for tablename in tuple(self._buffer.get_timeout(_time)):
            self._log.info("Flush (timeout) {}".format(tablename))
            self.flush_one(tablename)

    def finish(self):
        self._log.debug("finish")

        for k in tuple(self._buffer.keys()):
            self._log.info("Flush (finish) {}".format(k))
            self.flush_one(k)

        if self._database_adapter.is_connected():
                self._database_adapter.close()
        

    