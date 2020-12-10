from feedo.abstract_action import AbstractAction
from feedo.event import Event

# duplicate event with a new tag

class FilterTee(AbstractAction):
    def __init__(self, match, new_tag):
        AbstractAction.__init__(self, match)
        self._tag = new_tag

    def do(self, event):
        return [Event(event.tag, event.timestamp, event.record), Event(self._tag, event.timestamp, event.record)]








