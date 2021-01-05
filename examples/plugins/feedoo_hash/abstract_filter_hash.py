from feedoo.abstract_action import AbstractAction
from feedoo.event import Event

# hash value owns by a key

class AbstractFilterHash(AbstractAction):
    def __init__(self, match, key, output_key, hash_class):
        AbstractAction.__init__(self, match)
        self._key = key
        self._output_key = output_key
        self._format = format
        self._hash_class = hash_class

    def do(self, event):
        record = dict(event.record)
        # ignore case if key is not available
        if self._key in record:
            raw_data = record[self._key]
            if isinstance(raw_data, str):
                raw_data = str(raw_data)
            data = bytes(raw_data, "utf8")
            record[self._output_key] = self._hash_class(data).hexdigest()
        
        return Event(event.tag, event.timestamp, record)






