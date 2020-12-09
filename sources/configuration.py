import yaml
import unittest
import pprint
import logging
from glob import glob
import string

def loader(filename):
    with open(filename) as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)

    return data


class FormatDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"

class Configuration:
    def __init__(self):
        self._structure = {}
        self._log = logging.getLogger("Configuration")

    def load(self, filename, _loader=loader):
        self._structure = _loader(filename)
        self._structure["pipelines"] = self._structure.get("pipelines", {})
        self._structure["variables"] = self._structure.get("variables", {})
        self.include_pipelines(_loader)
        self._log.debug("variables : {} ".format(pprint.pformat(self._structure["variables"]) ))
        self._structure["pipelines"] = self.interpolate(self._structure["pipelines"], self._structure["variables"])

    def include_pipelines(self, _loader=loader):
        if self._structure.get("include") is not None:
            paths = list(glob(self._structure["include"]))
            for path in paths:
                self._log.debug("include {}".format(path))
                self._structure["pipelines"][path] = _loader(path)
            if len(paths) == 0:
                self._log.warning("{} doesn't match any file".format(self._structure["include"]))
        else:
            self._log.debug("no include path")
        
    def iterate_pipelines(self):

        for pipeline_id, pipeline in self._structure["pipelines"].items():
            self._log.debug("pipeline of {} : {} ".format(pipeline_id, pprint.pformat(pipeline) ))

            yield (pipeline_id, pipeline)

    def interpolate(self, input_structure, variables):

        if isinstance(input_structure, dict):
            input_structure = dict(input_structure)
            for k, v in input_structure.items():
                input_structure[k] = self.interpolate(v, variables)

        elif isinstance(input_structure, list):
            input_structure = list(input_structure)
            for i,v in enumerate(input_structure):
                input_structure[i] = self.interpolate(v, variables)

        elif isinstance(input_structure, str):
            try:
                fd = FormatDict(variables)
                formatter = string.Formatter()
                input_structure = formatter.vformat(input_structure, (), fd)
            except Exception as e:
                self._log.info("Fail to interpolate '{}' ({})".format(input_structure, e))

        return input_structure


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

