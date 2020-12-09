import json
import unittest
from abstract_action import AbstractAction
from event import Event

# parse a string as json

class ActionParserJson(AbstractAction):
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


class TestActionParserJson(unittest.TestCase):
    def test_dict_tree(self):
        action = ActionParserJson("*", "value", "tree")
        event = Event("tag", 123456789, {"key":"Z", "value":'{"aaa": "bb"}'})
        result = action.do(event)
        expected = {"key":"Z", "value":{"aaa":"bb"}}

        self.assertEqual(result.record, expected)

    def test_dict_add(self):
        action = ActionParserJson("*", "value", "add")
        event = Event("tag", 123456789, {"key":"Z", "value":'{"aaa": "bb"}'})
        result = action.do(event)
        expected = {"key":"Z", "value":'{"aaa": "bb"}', "aaa":"bb"}

        self.assertEqual(result.record, expected)

    def test_dict_merge(self):
        action = ActionParserJson("*", "value", "merge")
        event = Event("tag", 123456789, {"key":"Z", "value":'{"aaa": "bb"}'})
        result = action.do(event)
        expected = {"key":"Z", "aaa":"bb"}

        self.assertEqual(result.record, expected)

    def test_dict_merge_2(self):
        parameters = {"key":"value", "mode":"merge"}
        action = ActionParserJson("*", **parameters)
        event = Event("tag", 123456789, {"key":"Z", "value":'{"aaa": "bb"}'})
        result = action.do(event)
        expected = {"key":"Z", "aaa":"bb"}

        self.assertEqual(result.record, expected)





