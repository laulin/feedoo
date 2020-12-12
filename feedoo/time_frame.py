from time import time
import pprint

class TimeFrame:
    def __init__(self, windows:int):
        # windows is the number of second
        self._windows = windows
        self._fifo = []

    def add_event(self, event, timestamp=None, _time=time):
        if timestamp is None:
            ts = int(_time())
        else:
            ts = timestamp

        tmp = (ts, event)
        self._fifo.append(tmp)

        return self.update(_time)
 

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
        return output

    def flush(self):
        self._fifo = []

    def __len__(self):
        return len(self._fifo)

    def __repr__(self):
        return pprint.pformat(self._fifo)
        