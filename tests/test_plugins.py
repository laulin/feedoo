from feedo.plugins import Plugins
import feedo.input

import unittest
from pprint import pprint
import logging


class TestPlugins(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def test_snake_to_camel(self):
        p = Plugins()
        result = p.snake_to_camel_case("this_is_my_class")
        expected = "ThisIsMyClass"

        self.assertEqual(result, expected)

    def test_load_from_package(self):
        p = Plugins()
        result = p.load_from_package(feedo.input, "input_")

        self.assertNotEqual(len(result), 0)

    def test_load_vanilla(self):
        p = Plugins()
        result = p.load_vanilla()
        pprint(result)

    