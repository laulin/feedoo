from feedoo.abstract_action import AbstractAction
from feedoo.hash_storage import HashStorage
import time
from functools import partial
from feedoo.event import Event
from feedoo.time_frame import TimeFrame

# This rule matches when there are at least a certain number of events in a given time frame. This may be counted on a per-query_key basis.

class FilterFrequency(AbstractAction):
    def __init__(self, match, tag, alert, num_events, timeframe, query_key=None, db_path=None):
        AbstractAction.__init__(self, match)
        
        self._query_key = query_key
        self._tag = tag
        self._match = match
        self._alert = alert
        self._num_events = num_events
        self._timeframe = timeframe
        self._state = HashStorage(db_path, timeout=timeframe)

    def do(self, event):
        record = event.record

        if self._query_key is None:
            query_key = ""
        else:
            query_key = event.record.get(self._query_key)

        if query_key is None:
            return event

        if query_key not in self._state:
            self._state[query_key] = TimeFrame(self._timeframe)

        time_frame = self._state[query_key]
        time_frame.add_event(event)
        self._state[query_key] = time_frame

        if len(self._state[query_key]) >= self._num_events:
            timestamp = int(time.time())
            new_record = {
                "timestamp" : timestamp,
                "num_events" : len(self._state[query_key]),
                "timeframe" : self._timeframe
            }

            new_record.update(self._alert)
            new_event = Event(self._tag, timestamp, new_record)            

            return [event, new_event]
        
        return event

    def update(self, _time=time.time):
        for query_key in tuple(self._state.get_timeout(_time)):
            del self._state[query_key]
