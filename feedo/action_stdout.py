from .abstract_action import AbstractAction
from .event import Event

# parse a date field and transform it

class ActionStdout(AbstractAction):
    def __init__(self, match):
        AbstractAction.__init__(self, match)
        
    def do(self, event):
        to_print = "{}[{}]: {}".format(event.tag, event.timestamp, event.record)
        print(to_print)
        self._log.info(to_print)
        return event
