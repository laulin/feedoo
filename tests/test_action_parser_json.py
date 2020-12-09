import unittest
from feedo.action_parser_json import ActionParserJson
from feedo.event import Event

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





