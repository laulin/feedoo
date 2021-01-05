from feedoo.abstract_action import AbstractAction
from feedoo.event import Event
import hashlib

# MD5 sum of a key

class FilterMD5(AbstractAction):
    def __init__(self, match, key, output_key):
        AbstractAction.__init__(self, match)
        self._key = key
        self._output_key = output_key
        self._format = format

    def do(self, event):
        record = dict(event.record)
        # ignore case if key is not available
        if self._key in record:
            raw_data = record[self._key]
            if isinstance(raw_data, str):
                raw_data = str(raw_data)
            data = bytes(raw_data, "utf8")
            record[self._output_key] = hashlib.md5(data).hexdigest()
        
        return Event(event.tag, event.timestamp, record)






