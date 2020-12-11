import argparse


def get_args(argv=None):
    parser = argparse.ArgumentParser(description='Feedoo is an ETL for rethinkdb')
    parser.add_argument("-c", "--config", help="set the configuration file path", default="/etc/feedoo/default.yaml", dest="configuration_path")
    parser.add_argument('--verbose', '-v', action='count', default=0, help="verbose", dest="verbosity")
    return parser.parse_args(argv)
