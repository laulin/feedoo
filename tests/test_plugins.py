from feedo.plugins import Plugins
import feedo.input

import unittest
import logging


class TestPlugins(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def test_snake_to_camel(self):
        p = Plugins()
        result = p.snake_to_camel_case("this_is_my_class")
        expected = "ThisIsMyClass"

        self.assertEqual(result, expected)

    def test_test(self):
        p = Plugins()
        modules = p.load_from_package(feedo.input)

        for basename, func in modules.items():
            print("{} : {} -> {}".format(basename, func, func()))
