from feedoo.abstract_action import AbstractAction
from feedoo.hash_storage import HashStorage
import time
from functools import partial
from feedoo.event import Event
from feedoo.time_frame import TimeFrame
from pprint import pprint


# This action matches when the volume of events during a given time period is spike_height times
# larger or smaller than during the previous time period. It uses two sliding windows to compare 
# the current and reference frequency of events. We will call this two windows “reference” and “current”.

class FilterSpike(AbstractAction):
    SPIKE_TYPE = ["up", "down", "both"]
    def __init__(self, match, tag, alert, spike_height, spike_type, timeframe, query_key=None, field_value=None, threshold_ref=10, threshold_cur=10, db_path=None):
        AbstractAction.__init__(self, match)
        
        self._tag = tag
        self._match = match
        self._alert = alert
        self._spike_height = spike_height
        self._spike_type = spike_type
        if spike_type not in FilterSpike.SPIKE_TYPE:
            raise Exception("Invalid spike type : {}, expect {}".format(spike_type, FilterSpike.SPIKE_TYPE))
        self._timeframe = timeframe
        self._field_value = field_value
        self._query_key = query_key
        self._threshold_ref = threshold_ref
        self._threshold_cur = threshold_cur

        self._state = HashStorage(db_path, timeout=timeframe*2)

    def do(self, event, _time=time.time):
        query_key = self.get_query_key_value(event)       
        if  query_key is None:
            return event

        self._push_event_or_field(query_key, event, _time)
        matched = (False, None, None)
        try:
            matched = self._compare_current_and_reference(query_key)
        except ZeroDivisionError:
            pass

        if matched[0]:
            timestamp = int(time.time())
            new_record = {
                "timestamp" : timestamp,
                "spike_height" : matched[2],
                "spike_type" : matched[1]
            }

            new_record.update(self._alert)
            new_event = Event(self._tag, timestamp, new_record)            

            return [event, new_event]
        
        return event

    def update(self, _time=time.time):
        for query_key in tuple(self._state.get_timeout(_time)):
            del self._state[query_key]


    def get_query_key_value(self, event):
        if self._query_key is None:
            query_key = ""
        else:
            query_key = event.record.get(self._query_key)

        return query_key

    def _push_event_or_field(self, query_key, event, _time=time.time):

        value = event
        if self._field_value is not None :
            value = event.record.get(self._field_value, 0)
        
        if query_key not in self._state:
            time_frame_2 = TimeFrame(self._timeframe*2)
            time_frame_1 = TimeFrame(self._timeframe*1, time_frame_2)
            self._state[query_key] = [time_frame_1, time_frame_2]

        time_frames = self._state[query_key]
        timeouted = time_frames[0].add_event(value, _time=_time)
        self._state[query_key] = time_frames

    def _compare_current_and_reference(self, query_key):
        # ZeroDivisionError must be catched and be considered as false 
        current_length = len(self._state[query_key][0])
        reference_length = len(self._state[query_key][1])

        if current_length < self._threshold_cur or reference_length < self._threshold_ref:
            return (False, None, None)

        if self._field_value is None:
            current_value = current_length
            reference_value = reference_length
        else:
            current_value = self._state[query_key][0].average()
            reference_value = self._state[query_key][1].average()

        ratio = current_value / reference_value
        if self._spike_type in ["up", "both"]:
            if ratio >= self._spike_height:
                return (True , "up", ratio)

        if self._spike_type in ["down", "both"]:
            if (1.0/ratio) >= self._spike_height:
                return (True , "down", ratio)

        return (False, None, None)
            
                
