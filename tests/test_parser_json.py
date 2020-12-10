import unittest
from feedo.parser.parser_json import ParserJson
from feedo.event import Event

class TestParserJson(unittest.TestCase):
    def test_dict_tree(self):
        action = ParserJson("*", "value", "tree")
        event = Event("tag", 123456789, {"key":"Z", "value":'{"aaa": "bb"}'})
        result = action.do(event)
        expected = {"key":"Z", "value":{"aaa":"bb"}}

        self.assertEqual(result.record, expected)

    def test_dict_add(self):
        action = ParserJson("*", "value", "add")
        event = Event("tag", 123456789, {"key":"Z", "value":'{"aaa": "bb"}'})
        result = action.do(event)
        expected = {"key":"Z", "value":'{"aaa": "bb"}', "aaa":"bb"}

        self.assertEqual(result.record, expected)

    def test_dict_merge(self):
        action = ParserJson("*", "value", "merge")
        event = Event("tag", 123456789, {"key":"Z", "value":'{"aaa": "bb"}'})
        result = action.do(event)
        expected = {"key":"Z", "aaa":"bb"}

        self.assertEqual(result.record, expected)

    def test_dict_merge_2(self):
        parameters = {"key":"value", "mode":"merge"}
        action = ParserJson("*", **parameters)
        event = Event("tag", 123456789, {"key":"Z", "value":'{"aaa": "bb"}'})
        result = action.do(event)
        expected = {"key":"Z", "aaa":"bb"}

        self.assertEqual(result.record, expected)





