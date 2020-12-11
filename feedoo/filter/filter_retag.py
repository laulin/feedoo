from feedoo.abstract_action import AbstractAction
from feedoo.event import Event

# retag an event with contant value or key

class FilterRetag(AbstractAction):
    def __init__(self, match, value, key=None):
        AbstractAction.__init__(self, match)
        self._value = value
        self._key = key

    def do(self, event):
        record = event.record
        new_tag = record.get(self._key, self._value)
        return Event(new_tag, event.timestamp, event.record)
