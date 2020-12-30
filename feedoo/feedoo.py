from feedoo.configuration import Configuration
from feedoo.feed_manager import FeedManager 
from feedoo.cli import get_args
import logging
import sys

def main():
    args = get_args()

    log_format = '[%(asctime)s] %(processName)s : %(levelname)s %(name)s %(message)s'
    if args.verbosity == 0:
        logging.basicConfig(level=logging.WARNING, format=log_format)
    elif args.verbosity == 1:
        logging.basicConfig(level=logging.INFO, format=log_format)
    elif args.verbosity == 2:
        logging.basicConfig(level=logging.DEBUG, format=log_format)
    else:
        logging.basicConfig(level=logging.NOTSET, format=log_format)

    configuration = Configuration()
    configuration.load(args.configuration_path)

    feed_manager = FeedManager(configuration)
    feed_manager.setup()
    feed_manager.drop_privileges()
    feed_manager.loop()

if __name__ == "__main__":
    main()
