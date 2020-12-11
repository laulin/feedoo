import json
from feedoo.abstract_action import AbstractAction
from feedoo.event import Event

# parse a string as json

class ParserJson(AbstractAction):
    def __init__(self, match, key, mode="merge"):
        AbstractAction.__init__(self, match)
        self._key = key
        self._mode = mode

    def do(self, event):
        record = dict(event.record)
        to_parse = record.get(self._key)
        if to_parse is None:
            self._log.debug("Failed to parse '{}', key doesn't exist".format(to_parse))
            return
        try:
            result = json.loads(to_parse)
        except JSONDecodeError:
            self._log.debug("Failed to parse '{}'".format(to_parse))
            return 
 
        if self._mode == "tree":
            record[self._key] = result
        elif self._mode == "merge":
            del record[self._key]
            record.update(result)
        elif self._mode == "add":
            record.update(result)
        else:
            raise Exception("Bad mode '{}'".format(self._mode))
            
        return Event(event.tag, event.timestamp, record)
