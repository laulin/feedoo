from time import time
import pprint

class TimeFrame:
    def __init__(self, windows:int):
        # windows is the number of second
        self._windows = windows
        self._fifo = []

    def add_event(self, event, _time=time):
        timestamp = int(_time())
        tmp = (timestamp, event)
        self._fifo.append(tmp)
        self.update(_time)

    def update(self, _time=time):
        reference_time = int(_time()) - self._windows
        filtered = filter(lambda x : x[0]>reference_time, self._fifo)
        self._fifo = list(filtered)

    def flush(self):
        self._fifo = []

    def __len__(self):
        return len(self._fifo)

    def __repr__(self):
        return pprint.pformat(self._fifo)
        