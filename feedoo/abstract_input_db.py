from feedoo.abstract_action import AbstractAction
from feedoo.hash_storage import HashStorage
import time
from functools import partial
from fnmatch import fnmatch
from feedoo.event import Event
from feedoo.intervals import iterate_intervals
from pprint import pprint

class AbstractInputDB(AbstractAction):
    def __init__(self, tag:str, windows:int, time_key:str, table_name_match:str, offset:int=0, remove=False, reload_position=False, db_path=None):
        AbstractAction.__init__(self)
        self._database_adapter = None
        self._time_key = time_key
        self._windows = windows
        self._table_name_match = table_name_match
        self._offset = offset
        self._remove = remove
        self._reload_position = reload_position
        self._position = HashStorage(db_path)
        self._tag = tag

        self._start = True
    
    def do(self, event):
        # directly forward
        return event

    def get_table_matching(self, tables):
        # return matching tables
        match_funct = lambda x: fnmatch(x, self._table_name_match)
        return filter(match_funct, tables)

    def get_time_range(self, tables):
        # per table, get min and max timestamp
        time_range = list()

        for table in tables:
            min_ts = self._database_adapter.get_min(table, self._time_key)
            max_ts = self._database_adapter.get_max(table, self._time_key)
            time_range.append((table, min_ts, max_ts))

        time_range = sorted(time_range, key=lambda x : x[2])
        return time_range

    def iterate_time_range(self, time_range:list, start_time:int, stop_time:int):
        segments = map(lambda x : (x[1], x[2]), time_range)
        tables = map(lambda x : x[0], time_range)
        windows = iterate_intervals(start_time, stop_time-1, self._windows, segments)
        intervals = filter(lambda x : x[1] is not None, zip(tables, windows))
        for table, interval_list in intervals:
            for start, end in interval_list:
                yield table, start, end     

    def process_window(self, table, min_ts, max_ts, _time=time.time):
        documents = self._database_adapter.get_time_serie(table, self._time_key, min_ts, max_ts)
        #self._log.debug("Process windows [{}, {}] in table {} with {} documents".format(min_ts, max_ts, table, len(documents)))
        for document in documents:
            event = Event(self._tag, int(_time()), document)
            self.call_next(event)

        if self._remove:
            #self._log.info("Delete {} documents from {} to {} in {}".format(len(documents), min_ts, max_ts, table))
            self._database_adapter.delete_time_serie(table, self._time_key, min_ts, max_ts)
            if self._database_adapter.is_table_empty(table):
                self._log.info("Delete table {}".format(table))
                self._database_adapter.delete_table(table)


    def process_multiple_windows(self, from_timestamp, to_timestamp):
        all_tables = self._database_adapter.list_tables()
        tables = self.get_table_matching(all_tables)
        time_range = self.get_time_range(tables)
        for table, min_ts, max_ts in self.iterate_time_range(time_range, from_timestamp, to_timestamp):

            self.process_window(table, min_ts, max_ts)

        return max_ts

    def update(self, _time=time.time):

        current_time = _time() + self._offset
        if self._start:
            self._start = False
            self._database_adapter.connect()

            if self._reload_position:
                position = self._position.get("position", 0)
                self._log.info("Reload from timestamp {}".format(position))
                self._position["position"] = self.process_multiple_windows(position, current_time)
            else:
                self._position["position"] = current_time
                self._log.info("Reload at current time + offset {}".format(current_time))
        else:
            if current_time - self._position["position"] >= self._windows:
                self._log.debug("current_time {}, position {}".format(current_time, self._position["position"]))
                self._position["position"] = self.process_multiple_windows(self._position.get("position", 0), current_time) +1

    def finish(self):
        self._database_adapter.close()
                

            
                