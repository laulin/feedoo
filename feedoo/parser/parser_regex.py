import re
import logging
from feedoo.abstract_action import AbstractAction
from feedoo.event import Event

# parse a string and return a dict
# dict' keys is defines by tag (?P<name>)

class ParserRegex(AbstractAction):
    def __init__(self, match, regex, key, mode="merge"):
        AbstractAction.__init__(self, match)
        self._regex = regex
        self._names = tuple(re.findall(r"\(\?P<(.+?)>", regex))
        self._key = key
        self._mode = mode
        self._log.info("Create regex parser with '{}', key={}, mode={}".format(regex, key, mode))

    def do(self, event):
        record = dict(event.record)
        to_parse = record.get(self._key)

        if to_parse is None:
            self._log.debug("Failed to parse '{}', key doesn't exist".format(to_parse))
            return

        result = self.match(to_parse)
        if result is None:
            return

        if self._mode == "tree":
            record[self._key] = result
        elif self._mode == "merge":
            del record[self._key]
            record.update(result)
        elif self._mode == "add":
            record.update(result)
        else:
            self._log.error("Bad mode '{}' ! (check the configuration)".format(self._mode))
            raise Exception("Bad mode '{}'".format(self._mode))
            
        return Event(event.tag, event.timestamp, record)

    def match(self, field):
        matched = re.match(self._regex, field)
        output = dict()

        if not matched:
            self._log.debug("Not matching '{}' and '{}'".format(self._regex, field))
            return

        for k in self._names:
            output[k] = matched.group(k) 

        return output

    def update(self):
        pass
