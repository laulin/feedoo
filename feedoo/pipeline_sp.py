import logging
import time

class PipelineSP:
    def __init__(self, actions):
        self._log = logging.getLogger("PipelineSP")
        self._pipeline = []
        self._actions = actions
        self._pipeline_id = None

    def create(self, pipeline_id, actions):
        pipeline = list()
        self._pipeline_id = pipeline_id

        for action in actions:
            name = action["name"]
            del action["name"]
            if name not in self._actions:
                self._log.error(name + " is not an available action")
                raise Exception(name + " is not an available action")
            action_class = self._actions[name]

            try:
                action = action_class(**action)
            except Exception as e:
                self._log.error("{} don't use parameter {}".format(action_class.__class__.__name__, e))
                self._log.error("dict : " + str(action))
                raise Exception("{} don't use parameter {}".format(action_class.__class__.__name__, e))

            pipeline.append(action)
            
        self._pipeline = pipeline
        self._connect_actions()

    def get_pipeline_id(self):
        return self._pipeline_id

    def _connect_actions(self):
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
                self._log.warning("action {} failed to update ({})".format(action.__class__.__name__, repr(e)))

        return self._is_changed()

    def finish(self):

        for action in self._pipeline:
            try:
                action.finish()
            except Exception as e:
                self._log.warning("action {} failed to finish ({})".format(action.__class__.__name__, repr(e)))

    def get_states(self):
        return self._pipeline_id, [a.get_states() for a in self._pipeline]

    def _is_changed(self):
        # return True if something happens in actions since last update
        output = False

        for a in self._pipeline:
            output |= a.get_changed()
            a.reset_changed()

        return output