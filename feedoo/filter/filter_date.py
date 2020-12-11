from chronyk import Chronyk
from feedoo.abstract_action import AbstractAction
from feedoo.event import Event

# parse a date field and transform it

class FilterDate(AbstractAction):
    def __init__(self, match, key, format=None):
        AbstractAction.__init__(self, match)
        self._key = key
        self._format = format

    def do(self, event):
        record = dict(event.record)
        time = Chronyk(record[self._key])
        if self._format is None:
            record[self._key] = time.timestamp()
        else:
            record[self._key] = time.timestring(self._format)

        return Event(event.tag, event.timestamp, record)






