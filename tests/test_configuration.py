import yaml
import string
import unittest
from feedo.configuration import Configuration
from feedo.configuration import FormatDict


EXAMPLE = """
"variables": 
    "IP" : "127.0.0.1"
    "PORT" : "28018"
"pipelines":
    "A":
        - name: Inputfile
          watch_path : "/tmp"
          path_pattern : ".*/test.log"
          remove: True
          tag : test

        - name : tee
          match : test
          new_tag : test.a

        - name : parser_regex
          regex : "(?P<date>.+?)       (?P<service>.+?)  (?P<json>\\\{.+?\\\})"
          match : test.a

        - name : "parser_json"
          key : "json"
          mode : "merge"
          match : test.a

        - name : remove_keys
          keys : "logtime"
          match : test.a

        - name : date 
          key : "date"
          match : test.a

        - name : tee
          match : test
          new_tag : test.b

        - name : parser_regex
          regex : "(?P<date>[^ ]+).+"
          match : test.b
        
        - name : date 
          key : date
          format : "%Y-%m-%d"
          match : test.b
"""

class TestConfiguration(unittest.TestCase):
    def test_1(self):
        data = yaml.load(EXAMPLE, Loader=yaml.SafeLoader)
        
    def test_2(self):
        def mock_loader(filename): return yaml.load(EXAMPLE, Loader=yaml.SafeLoader)

        configuration = Configuration()
        configuration.load(None, mock_loader)

    def test_interpolate_1(self):
        configuration = Configuration()

        data = {"x" : "example : {my_vars}"}
        variables = {"my_vars" : "y"}

        result = configuration.interpolate(data, variables)
        expected = data = {"x" : "example : y"}

        self.assertEqual(result, expected)

    def test_interpolate_2(self):
        configuration = Configuration()

        data = {"z" : {"x" : "example : {my_vars}"}}
        variables = {"my_vars" : "y"}

        result = configuration.interpolate(data, variables)
        expected = data = {"z" : {"x" : "example : y"}}

        self.assertEqual(result, expected)

    def test_interpolate_3(self):
        configuration = Configuration()

        data = {"z" : {"x" : [{"a" : "{ip}", "b" : "{port}"}]}}
        variables = {"ip" : "localhost", "port":"22"}

        result = configuration.interpolate(data, variables)
        expected = data = {"z" : {"x" : [{"a" : "localhost", "b" : "22"}]}}

        self.assertEqual(result, expected)

    def test_3(self):
        def mock_loader(filename): return yaml.load(EXAMPLE, Loader=yaml.SafeLoader)

        configuration = Configuration()
        configuration.load(None, mock_loader)
        result = list(configuration.iterate_pipelines())
        expected = [('A',
                    [{'name': 'Inputfile',
                        'path_pattern': '.*/test.log',
                        'remove': True,
                        'tag': 'test',
                        'watch_path': '/tmp'},
                    {'match': 'test', 'name': 'tee', 'new_tag': 'test.a'},
                    {'match': 'test.a',
                        'name': 'parser_regex',
                        'regex': '(?P<date>.+?)       (?P<service>.+?)  (?P<json>\\{.+?\\})'},
                    {'key': 'json', 'match': 'test.a', 'mode': 'merge', 'name': 'parser_json'},
                    {'keys': 'logtime', 'match': 'test.a', 'name': 'remove_keys'},
                    {'key': 'date', 'match': 'test.a', 'name': 'date'},
                    {'match': 'test', 'name': 'tee', 'new_tag': 'test.b'},
                    {'match': 'test.b', 'name': 'parser_regex', 'regex': '(?P<date>[^ ]+).+'},
                    {'format': '%Y-%m-%d', 'key': 'date', 'match': 'test.b', 'name': 'date'}])]


        self.assertEqual(result, expected)

    def test_missing_key(self):

        fd = FormatDict({"foo":"xxx"})
        s = '{foo} {bar}'
        formatter = string.Formatter()
        result = formatter.vformat(s, (), fd)

        self.assertEqual(result, "xxx {bar}")

