from chronyk import Chronyk
import os
import os.path
import logging
from contextlib import suppress
from feedoo.abstract_action import AbstractAction
from feedoo.event import Event
from feedoo.hash_storage import HashStorage
from time import time

class AbstractOutputFile(AbstractAction):
    def __init__(self, match, time_key, path_template, buffer_size=1000, timeout_flush=60, db_path=None):
        AbstractAction.__init__(self, match)
        self._time_key = time_key
        self._path_template = path_template
        self._buffer = HashStorage(db_path, timeout_flush)
        self._buffer_size = buffer_size

        self._last_flush = 0
        self._timeout_flush = timeout_flush

    def do(self, event):
        record = event.record
        if self._time_key is not None and self._time_key in record:
            current_time = Chronyk(record[self._time_key])
        else:
            current_time = Chronyk(time())

        path = current_time.timestring(self._path_template)
        path = path.format(**record)
        if path not in self._buffer:
            self._buffer[path] = list()

        self._buffer[path].append(record)

        if len(self._buffer[path]) > self._buffer_size:
            self.flush_one(path)

        return event

    def finish(self):
        self._log.debug("finish")

        for k in tuple(self._buffer.keys()):
            self._log.info("Flush (finish) {}".format(k))
            self.flush_one(k)
        self._buffer.dump()

    def flush_one(self, path):
        self._log.debug("flush to {}".format(path))

        with suppress(FileExistsError):
            directory = os.path.dirname(path)
            os.makedirs(directory, 0o755)

        with open(path, "a") as f:
            values = self._buffer[path]
            data = self.value_to_string(values)
            f.write(data)
            del self._buffer[path]

    def update(self, _time=time):
        if _time() - self._last_flush > self._timeout_flush:
            self._last_flush = _time()
            for path in tuple(self._buffer.keys()):
                self._log.info("Flush {}".format(path))
                self.flush_one(path)

    def value_to_string(self, values):
        raise NotImplemented()

