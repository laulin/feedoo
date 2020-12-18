from chronyk import Chronyk
from feedoo.abstract_action import AbstractAction
from feedoo.event import Event

# rename fields

class FilterRename(AbstractAction):
    def __init__(self, match:str, keys:dict):
        AbstractAction.__init__(self, match)
        self._keys = keys

    def do(self, event):
        record = dict(event.record)
        
        for old_key, new_key in self._keys.items():
            if old_key in record:
                record[new_key] = record[old_key]
                del record[old_key]

        return Event(event.tag, event.timestamp, record)






