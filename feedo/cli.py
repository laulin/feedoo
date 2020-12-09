import argparse
import unittest


def get_args(argv=None):
    parser = argparse.ArgumentParser(description='Feed is an ETL for rethinkdb')
    parser.add_argument("-c", "--config", help="set the configuration file path", default="/etc/feed/default.yaml", dest="configuration_path")
    parser.add_argument('--verbose', '-v', action='count', default=0, help="verbose", dest="verbosity")
    return parser.parse_args(argv)

class TestCli(unittest.TestCase):
    def test_cli_conf_file(self):
        args = get_args(["-c", "/etc/conf.yaml", "-vv"])
        self.assertEqual(args.configuration_path, "/etc/conf.yaml")

    def test_cli_verbose(self):
        args = get_args(["-c", "/etc/conf.yaml", "-vv"])
        self.assertEqual(args.verbosity, 2)