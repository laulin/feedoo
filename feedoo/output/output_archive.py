from chronyk import Chronyk
from collections import defaultdict
import os
import os.path
import shutil
import logging
from contextlib import suppress
from feedoo.abstract_action import AbstractAction
from feedoo.event import Event
from feedoo.hash_storage import HashStorage
from time import time

# push document to archive files

class OutputArchive(AbstractAction):
    def __init__(self, match, time_key, path_template, buffer_size=1000, timeout_flush=60, db_path=None, db_table="default_table"):
        AbstractAction.__init__(self, match)
        self._time_key = time_key
        self._path_template = path_template
        self._buffer = HashStorage(db_path, timeout_flush, db_table)
        self._buffer_size = buffer_size

        self._last_flush = 0
        self._timeout_flush = timeout_flush

    def do(self, event):
        record = event.record
        time = Chronyk(record[self._time_key])
        path = time.timestring(self._path_template)
        path = path.format(**record)
        if path not in self._buffer:
            self._buffer[path] = list()

        buffer = self._buffer[path] 
        buffer.append(record)
        self._buffer[path] = buffer

        if len(self._buffer[path]) > self._buffer_size:
            self.flush_one(path)

        return event

    def finish(self):
        self._log.debug("finish")

        for k in tuple(self._buffer.keys()):
            self._log.info("Flush (finish) {}".format(k))
            self.flush_one(k)

    def flush_one(self, path):
        self._log.debug("flush to {}".format(path))

        with suppress(FileExistsError):
            directory = os.path.dirname(path)
            os.makedirs(directory, 0o755)

        with open(path, "a") as f:
            values = self._buffer[path]
            data = "\n".join(map(str, values)) + "\n"
            f.write(data)
            del self._buffer[path]

    def update(self, _time=time):
        if _time() - self._last_flush > self._timeout_flush:
            self._last_flush = _time()
            for path in tuple(self._buffer.keys()):
                self._log.info("Flush {}".format(path))
                self.flush_one(path)

