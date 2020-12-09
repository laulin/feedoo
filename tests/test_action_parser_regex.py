import unittest
from feedo.action_parser_regex import ActionParserRegex
from feedo.event import Event


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





