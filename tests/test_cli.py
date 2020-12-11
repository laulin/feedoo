import unittest
from feedoo.cli import get_args


class TestCli(unittest.TestCase):
    def test_cli_conf_file(self):
        args = get_args(["-c", "/etc/conf.yaml", "-vv"])
        self.assertEqual(args.configuration_path, "/etc/conf.yaml")

    def test_cli_verbose(self):
        args = get_args(["-c", "/etc/conf.yaml", "-vv"])
        self.assertEqual(args.verbosity, 2)