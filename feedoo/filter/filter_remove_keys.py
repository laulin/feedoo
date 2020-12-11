from feedoo.abstract_action import AbstractAction
from feedoo.event import Event

# remove one or more keys of the document

class FilterRemoveKeys(AbstractAction):
    def __init__(self, match, keys):
        AbstractAction.__init__(self, match)
        self._keys = keys

    def do(self, event):
        record = dict(event.record)
        # if string
        if isinstance(self._keys, str):
            if self._keys in record:
                del record[self._keys]
        # if list/tuple
        else:
            for k in self._keys:
                if k in record:
                    del record[k]
                
        return Event(event.tag, event.timestamp, record)

