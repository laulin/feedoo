from feedoo.abstract_action import AbstractAction
from feedoo.event import Event
import time

# provide a fake source of event for test

class InputDummy(AbstractAction):
    def __init__(self, tag, data):
        AbstractAction.__init__(self)
        self._tag = tag
        self._data = data
        
    def do(self, event):
        return event

    def update(self):
        if self._data is None:
            return
        if isinstance(self._data, dict):
            event = Event(self._tag, int(time.time()), self._data)
            self.call_next(event)
            self._data = None
            return
        if isinstance(self._data, list):
            for data in self._data:
                event = Event(self._tag, int(time.time()), data)
                self.call_next(event)
                
            self._data = None
