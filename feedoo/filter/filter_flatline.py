from feedoo.abstract_action import AbstractAction
import time
from feedoo.hash_storage import HashStorage
from feedoo.time_frame import TimeFrame
from feedoo.event import Event

# This action matches when the total number of events is under a given threshold for a time period.

class FilterFlatline(AbstractAction):
    def __init__(self, match, tag, alert, threshold, timeframe, query_key=None, forget_keys=True, db_path=None):
        # match defines the pattern to be matched
        # tag is the alert tag
        # alert is a dict used to create alert
        # threshold is the minimum number of event in a time window
        # timeframe is the windows duration
        # query_key defines the key used to select event. This field must be present in all of the events that are checked.
        # forget_keys is used to remove query key if nothing append
        # db_path is used to store internal state in case of reloading
        AbstractAction.__init__(self, match)
        
        self._threshold = threshold
        self._timeframe = timeframe
        self._query_key = query_key
        self._tag = tag
        self._match = match
        self._alert = alert
        self._last_trigger = time.time() + timeframe
        self._forget_keys = forget_keys

        self._state = HashStorage(db_path, timeframe)

    def do(self, event, _time=time.time):
        
        query_key = self.get_query_key(event)
        if query_key is None :
            return event

        if query_key not in self._state:
            self._state[query_key] = TimeFrame(self._timeframe)

        time_frame = self._state[query_key]
        time_frame.add_event(event, _time=_time)
        self._state[query_key] = time_frame

        
        return event

    def get_query_key(self, event):
        if self._query_key is None:
            query_key = ""
        else:
            if self._query_key not in event.record:
                # no valid, ignore
                return None
            else:
                query_key = event.record[self._query_key]
        
        return query_key

    def update(self, _time=time.time):
        output = []
        if _time() > self._last_trigger:
            self._last_trigger = _time() + self._timeframe

            for query_key in self._state.keys():
                time_frame = self._state[query_key]
                time_frame.update(_time=_time)
                self._state[query_key] = time_frame

                if len(self._state[query_key]) < self._threshold:
                    timestamp = int(_time())
                    new_record = {
                        "timestamp" : timestamp,
                        "number_of_event" :len(self._state[query_key]),
                        "query_key" : query_key
                    }

                    new_record.update(self._alert)
                    new_event = Event(self._tag, timestamp, new_record)            

                    output.append(new_record)

            if self._forget_keys:
                for query_key in tuple(self._state.get_timeout(_time)):
                    del self._state[query_key]

        return output