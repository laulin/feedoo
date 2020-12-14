from time import time
import pprint

class TimeFrame:
    def __init__(self, windows:int, next_timeframe=None):
        # windows is the number of second
        # next_timeframe is the next time frame to be used when update timeout element
        self._windows = windows
        self._fifo = []
        self._next_timeframe = next_timeframe

    def add_event(self, event, timestamp=None, _time=time, _update=True):
        if timestamp is None:
            ts = int(_time())
        else:
            ts = timestamp

        tmp = (ts, event)
        self._fifo.append(tmp)

        if _update:
            return self.update(_time)
        else:
            return []
 
    def update(self, _time=time):
        reference_time = int(_time()) - self._windows
        output = list()
        new_fifo = list()

        for element in self._fifo:
            if element[0] >reference_time:
                new_fifo.append(element)
            else:
                output.append(element)

        self._fifo = new_fifo

        if self._next_timeframe is not None:
            for ts, v in output:
                self._next_timeframe.add_event(v, ts, _time, False)
            return self._next_timeframe.update(_time)

        return output

    def average(self):
        return sum(map(lambda x : x[1], self._fifo)) / len(self._fifo)

    def flush(self):
        self._fifo = []

    def __len__(self):
        return len(self._fifo)

    def __repr__(self):
        return pprint.pformat(self._fifo)
        