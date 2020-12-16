from feedoo.abstract_action import AbstractAction
from feedoo.hash_storage import HashStorage
import time
from functools import partial
from fnmatch import fnmatch
from feedoo.event import Event

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

    def iterate_time_range(self, time_range, start_time, stop_time):
        # return time window and table to be processed
        for table, min_ts, max_ts in time_range:
            if min_ts > stop_time or max_ts < start_time:
                # table is out of range
                pass
            else:            
                for window_start in range(min_ts, max_ts, self._windows):
                    window_end =  window_start+self._windows - 1
                    #self._log.debug("window_start {}".format(window_start))
                    # windows is too last
                    if window_start >= stop_time:
                        # self._log.debug("window_start {} > stop_time {} : end".format(window_start, stop_time))
                        # because time_range is monotonic in term of time, 
                        # nothing *must* appear after that point
                        return
                    # windows is too early
                    elif window_end < start_time:
                        # self._log.debug("window_end {} < start_time {} : continue".format(window_end, start_time))
                        pass
                    else:
                        # shrink to the minimum interval
                        clamp_start = max(window_start, start_time, min_ts)
                        clamp_end = min(window_end, stop_time, max_ts)
                        yield table, clamp_start, clamp_end
     

    def process_window(self, min_ts, max_ts, table, _time=time.time):
        documents = self._database_adapter.get_time_serie(table, self._time_key, min_ts, max_ts)
        self._log.debug("Process windows [{}, {}] in table {} with {} documents".format(min_ts, max_ts, table, len(documents)))

        for document in documents:
            event = Event(self._tag, int(_time()), document)
            self._log.debug("send event {}".format(event))
            self.call_next(event)

        if self._remove:
            self._database_adapter.delete_time_serie(table, self._time_key, min_ts, max_ts)
            if self._database_adapter.is_table_empty(table):
                self._database_adapter.delete_table(table)


    def process_multiple_windows(self, from_timestamp, to_timestamp):
        all_tables = self._database_adapter.list_tables()
        tables = self.get_table_matching(all_tables)
        time_range = self.get_time_range(tables)
        for table, min_ts, max_ts in self.iterate_time_range(time_range, from_timestamp, to_timestamp):

            self.process_window(min_ts, max_ts, table)

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
                

            
                