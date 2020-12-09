from chronyk import Chronyk
from .abstract_action import AbstractAction
from .event import Event

# retag an event with contant value or key

class ActionRetag(AbstractAction):
    def __init__(self, match, value, key=None):
        AbstractAction.__init__(self, match)
        self._value = value
        self._key = key

    def do(self, event):
        record = event.record
        new_tag = record.get(self._key, self._value)
        return Event(new_tag, event.timestamp, event.record)
