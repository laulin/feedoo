from feedoo.pipeline import Pipeline
from feedoo.plugins import Plugins
import unittest
from pprint import pprint

DOCUMENT_TEST = '2020-10-22T08:50:03+00:00       pihole.dnsmasq  {"type":"dnsmasq","tag":"pihole.dnsmasq","logtime":"Oct 22 10:50:03","log":"reply weu1-authgw.cloudapp.net is 13.94.251.244","source":"jarvis-2"}'

class TestPipeline(unittest.TestCase):
    def setUp(self):
        plugins = Plugins()
        self.actions = plugins.load_vanilla()
    def test_simple(self):
        actions = [
            {"name" : "input_dummy", "tag" : "my_pypeline", "data":{"log":"my log"}},
            {"name" : "output_stdout", "match" : "my_*"}
        ]
        pipeline = Pipeline(self.actions)
        pipeline.create("simple", actions)
        pipeline.update()

    def test_optimal(self):
        actions = [
            {"name" : "input_dummy", "tag" : "my_pipeline", "data":{"log":DOCUMENT_TEST}},
            {"name" : "parser_regex", "match" : "*", "key" : "log", "regex":"(?P<date>.+?)       (?P<service>.+?)  (?P<json>\{.+?\})"},
            {"name" : "parser_json", "match" : "*", "key":"json", "mode":"merge"},
            {"name" : "filter_remove_keys", "match" : "*", "keys":"logtime"},
            {"name" : "filter_date", "match" : "*", "key":"date"},
            {"name" : "output_stdout", "match" : "*"}
        ]
        pipeline = Pipeline(self.actions)
        pipeline.create("simple", actions)
        pipeline.update()

    def test_get_states(self):
        actions = [
            {"name" : "input_dummy", "tag" : "my_pypeline", "data":{"log":"my log"}},
            {"name" : "output_stdout", "match" : "my_*"}
        ]
        pipeline = Pipeline(self.actions)
        pipeline.create("simple", actions)
        pipeline.update()

        result = pipeline.get_states()

        expected = ('simple',
            [{'bypass': {},
            'do': {},
            'ignore': {},
            'in': {},
            'info': 'Dummy[my_pypeline]',
            'name': 'InputDummy',
            'out': {'my_pypeline': 1}},
            {'bypass': {},
            'do': {'my_pypeline': 1},
            'ignore': {},
            'in': {'my_pypeline': 1},
            'info': 'Stdout[my_*]',
            'name': 'OutputStdout',
            'out': {}}])

        self.assertEqual(result, expected)

