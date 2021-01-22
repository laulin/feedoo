from feedoo.abstract_action import AbstractAction
from feedoo.event import Event
import time

# parse a date field and transform it

class FilterGroupby(AbstractAction):
    def __init__(self, match:str, tag:str, keys:list, values:list=None, window:int=0, count:bool=False, unique:bool=False):
        AbstractAction.__init__(self, match)
        self._keys = keys
        self._values = values
        self._tag = tag
        self._count = count
        self._unique = unique
        self._last_update = 0
        self._window = window
        self._storage = dict()


    def do(self, event):
        record = dict(event.record)
        master_key = tuple()
        for k in self._keys:
            if k in record:
                master_key += (record[k],)
                del record[k]
            else:
                master_key += ("None",)
        

        self._storage.setdefault(master_key, list()).append(tuple(record.get(x) for x in self._values))

        return event

    def keep_unique(self, data:dict):
        output = dict()

        for k, v in data.items():
            output[k] = list(set(v))

        return output

    def count(self, data:dict):
        output = dict()

        for k, v in data.items():
            output[k] = len(v)

        return output

    def to_next(self, data:dict, _time=time.time):
        for k, v in data.items():
            record = dict(zip(self._keys, k))
            if isinstance(v, list):
                record["value"] = [dict(zip(self._values, x)) for x in sorted(v)]
            else:
                record["value"] = v
            event = Event(self._tag, int(_time()), record)
            self.call_next(event)

    def update(self, _time=time.time):
        if _time() - self._last_update > self._window:
            self._last_update = _time()

            tmp = self._storage

            if self._unique:
                tmp = self.keep_unique(tmp)

            if self._count:
                tmp = self.count(tmp)

            self.to_next(tmp, _time)
            
            self._storage.clear()