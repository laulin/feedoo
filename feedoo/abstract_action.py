from fnmatch import fnmatch
import logging

from feedoo.action_states import ActionStates

class AbstractAction:
    """
    this class describe the interface of action
    """
    def __init__(self, match=None):
        self._next = None
        self._match = match
        self._log = logging.getLogger(str(self.__class__.__name__))
        self._states = ActionStates(str(self.__class__.__name__), self.info)

    def set_next(self, next):
        """
        set the next action to be done after this one
        """
        self._next = next

    def call_next(self, event):
        """
        send event to the next element if existing
        """
        if self._next is not None:
            self._states.add_out(event)
            self._next.receive(event)

    def call_next_bypass(self, event):
        """
        send event to the next element if existing
        """
        if self._next is not None:
            self._states.add_bypass(event)
            self._next.receive(event)

    def update(self):
        """
        update internal state or flush event 
        """
        pass

    def finish(self):
        """
        called when the pipeline is destroyed to prevent internal state to be lost
        """
        pass

    def receive(self, event):
        """
        event containts tag, timestamp and record
        """
        self._states.add_in(event)
        if self._match is None or fnmatch(event.tag, self._match) == False:
            #self._log.debug("{} not matching with {}, shortcut".format(event.tag, self._match))
            self.call_next_bypass(event)
            return
        self._log.debug("{}.do({}) (filter : {})".format(self.__class__.__name__, event, self._match))
        self._states.add_do(event)
        try:
            new_event = self.do(event)
        except Exception as e:
            self._log.warning("self.do failed : "+getattr(e, 'message', repr(e)))
            raise e

        if new_event is None:
            # drop the event
            return
        elif isinstance(new_event, list): # must not use tuple for multiple events
            # creation of multiple event
            [self.call_next(e) for e in new_event]
        else:
            # forward the new event
            self.call_next(new_event)

    def do(self, event):
        # transparent action
        return event

    def get_states(self):
        return self._states.get_states()

    def info(self):
        return "undefined for {}".format(str(self.__class__.__name__))