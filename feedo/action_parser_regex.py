import re
import unittest
import logging
from abstract_action import AbstractAction
from event import Event

# parse a string and return a dict
# dict' keys is defines by tag (?P<name>)

class ActionParserRegex(AbstractAction):
    def __init__(self, match, regex, key, mode="merge"):
        AbstractAction.__init__(self, match)
        self._regex = regex
        self._names = tuple(re.findall(r"\(\?P<(.+?)>", regex))
        self._key = key
        self._mode = mode
        #self._log = logging.getLogger("ParserRegex")
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


class TestActionParserRegex(unittest.TestCase):
    def test_dict_tree(self):
        action = ActionParserRegex("*", r"(?P<x>a+) (?P<y>b+)", "value", "tree")
        event = Event("tag", 123456789, {"key":"Z", "value":"aaa bb"})
        result = action.do(event)
        expected = {"key":"Z", "value":{"x":"aaa", "y":"bb"}}

        self.assertEqual(result.record, expected)

    def test_dict_add(self):
        action = ActionParserRegex("*", r"(?P<x>a+) (?P<y>b+)", "value", "add")
        event = Event("tag", 123456789, {"key":"Z", "value":"aaa bb"})
        result = action.do(event)
        expected = {"key":"Z", "value":"aaa bb", "x":"aaa", "y":"bb"}

        self.assertEqual(result.record, expected)

    def test_dict_merge(self):
        action = ActionParserRegex("*", r"(?P<x>a+) (?P<y>b+)", "value", "merge")

        event = Event("tag", 123456789, {"key":"Z", "value":"aaa bb"})
        result = action.do(event)
        expected = {"key":"Z", "x":"aaa", "y":"bb"}

        self.assertEqual(result.record, expected)

    def test_dict_merge_2(self):
        parameters = {"key":"value", "mode":"merge"}
        action = ActionParserRegex("*", r"(?P<x>a+) (?P<y>b+)", **parameters)
        event = Event("tag", 123456789, {"key":"Z", "value":"aaa bb"})
        result = action.do(event)
        expected = {"key":"Z", "x":"aaa", "y":"bb"}

        self.assertEqual(result.record, expected)

    def test_from_log_ram(self):
        parameters = {"key":"log", "mode":"merge"}
        action = ActionParserRegex("*", r"(?P<date>.+?)\s+sys.ram\s+(?P<json>.+)", **parameters)
        event = Event("tag", 123456789, {"log":'2020-11-02T07:50:04+00:00        sys.ram {"tag":"sys.ram","Mem.free":774748,"Swap.free":102396,"Mem.total":3919812,"source":"jarvis-2","Swap.total":102396,"Swap.used":0,"Mem.used":3145064}'})
        result = action.do(event)
        expected = {'date': '2020-11-02T07:50:04+00:00',
                    'json': '{"tag":"sys.ram","Mem.free":774748,"Swap.free":102396,"Mem.total":3919812,"source":"jarvis-2","Swap.total":102396,"Swap.used":0,"Mem.used":3145064}'}

        self.assertEqual(result.record, expected)





