import logging

from .event import Event

from .action_date import ActionDate
from .action_parser_json import ActionParserJson
from .action_parser_regex import ActionParserRegex
from .action_remove_keys import ActionRemoveKeys
from .action_rethinkdb import ActionRethinkdb
from .action_archive import ActionArchive
from .action_stdout import ActionStdout
from .action_dummy import ActionDummy
from .action_tee import ActionTee
from .action_retag import ActionRetag
from .action_change import ActionChange
from .input_file import InputFile

CLASS_TABLE = {
    "date": ActionDate,
    "parser_json": ActionParserJson,
    "parser_regex": ActionParserRegex,
    "remove_keys": ActionRemoveKeys,
    "rethinkdb": ActionRethinkdb,
    "archive": ActionArchive,
    "dummy": ActionDummy,
    "stdout": ActionStdout,
    "tee": ActionTee,
    "retag": ActionRetag,
    "change": ActionChange,
    "input_file": InputFile
}

class Pipeline:
    def __init__(self):
        self._log = logging.getLogger("Pipeline")
        self._pipeline = []

    def create(self, actions):
        pipeline = list()

        for action in actions:
            name = action["name"]
            del action["name"]
            if name not in CLASS_TABLE:
                self._log.error(name + " is not an available action")
                raise Exception(name + " is not an available action")
            action_class = CLASS_TABLE[name]

            try:
                action = action_class(**action)
            except Exception as e:
                self._log.error("{} don't use parameter {}".format(action_class.__class__.__name__, e))
                self._log.error("dict : " + str(action))
                raise Exception("{} don't use parameter {}".format(action_class.__class__.__name__, e))

            pipeline.append(action)
            
        self._pipeline = pipeline
        self.connect_actions()

    def connect_actions(self):
        """
        chain each action to the next one
        """
        for action, action_next in zip(self._pipeline[0:-1], self._pipeline[1:]):
            action.set_next(action_next)

    def update(self):
        for action in self._pipeline:
            try:
                action.update()
            except Exception as e:
                self._log.warning("action {} failed to update ({})".format(action.__class__.__name__, e))

    def finish(self):
        for action in self._pipeline:
            try:
                action.finish()
            except Exception as e:
                self._log.warning("action {} failed to finish ({})".format(action.__class__.__name__, e))
