import inotify.adapters
import os.path
import os
import fnmatch
from glob import glob
from feedoo.abstract_action import AbstractAction
from feedoo.event import Event
from time import time


class InputFile(AbstractAction):
    def __init__(self, tag, watch_path, path_pattern, remove=False):
        AbstractAction.__init__(self)
        self._tag = tag
        self._watch_path = watch_path
        self._path_pattern = path_pattern
        self._watcher = None
        self._remove = remove

    def update(self):
        if self._watcher is None:
            # first run
            self._watcher = inotify.adapters.InotifyTree(self._watch_path)
            self._log.debug("First run, finding fitting file with '{}'".format(self._path_pattern))
            for filename in glob(self._path_pattern):
                self._log.debug("->{}".format(self._path_pattern))
                self.process_file("", filename)

        for event in self._watcher.event_gen():
            if event is None:
                return

            if 'IN_CLOSE_WRITE' in event[1]:
                self.process_file(event[2], event[3])

    def process_file(self, directory, filename):
        path = os.path.join(directory, filename)
        match = fnmatch.fnmatch(path, self._path_pattern)
        if match:
            self._log.info ("Process file '{}'".format(path))
            with open(path) as f:
                line_number = 0
                for line in f:
                    data = line.rstrip()
                    event = Event(self._tag, int(time()), {"log":data})
                    self.call_next(event)
                    line_number += 1
                self._log.info("Processing file '{}' produce {} events".format(filename, line_number))

            if self._remove:
                self._log.debug ("Remove file '{}'".format(path))
                os.remove(path)
