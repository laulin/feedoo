from feedo.pipeline import Pipeline
import unittest

DOCUMENT_TEST = '2020-10-22T08:50:03+00:00       pihole.dnsmasq  {"type":"dnsmasq","tag":"pihole.dnsmasq","logtime":"Oct 22 10:50:03","log":"reply weu1-authgw.cloudapp.net is 13.94.251.244","source":"jarvis-2"}'

class TestPipeline(unittest.TestCase):
    def test_simple(self):
        actions = [
            {"name" : "dummy", "tag" : "my_pypeline", "data":{"log":"my log"}},
            {"name" : "stdout", "match" : "my_*"}
        ]
        pipeline = Pipeline()
        pipeline.create(actions)
        pipeline.update()

    def test_optimal(self):
        actions = [
            {"name" : "dummy", "tag" : "my_pipeline", "data":{"log":DOCUMENT_TEST}},
            {"name" : "parser_regex", "match" : "*", "key" : "log", "regex":"(?P<date>.+?)       (?P<service>.+?)  (?P<json>\{.+?\})"},
            {"name" : "stdout", "match" : "*"},
            {"name" : "parser_json", "match" : "*", "key":"json", "mode":"merge"},
            {"name" : "remove_keys", "match" : "*", "keys":"logtime"},
            {"name" : "date", "match" : "*", "key":"date"}
        ]
        pipeline = Pipeline()
        pipeline.create(actions)
        result = pipeline.update()
        # expected = {'date': 1603356603.0, 'service': 'pihole.dnsmasq', 'type': 'dnsmasq', 'tag': 'pihole.dnsmasq', 'log': 'reply weu1-authgw.cloudapp.net is 13.94.251.244', 'source': 'jarvis-2'}

        # self.assertEqual(result.record, expected)