import logging
from pprint import pprint
import multiprocessing
import time
import signal

class PipelineMP:
    def __init__(self, actions):
        self._log = logging.getLogger("PipelineMP")
        self._pipeline = []
        self._actions = actions
        self._pipeline_id = None
        self._running = multiprocessing.Event()
        self._running.clear()
        self._process = None
        self._manager = multiprocessing.Manager()
        self._actions_states = self._manager.dict()

    def _create(self, pipeline_id, actions):
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

    def _process_kernel(self, pipeline_id, actions):
        self._create(pipeline_id, actions)

        self._log.info("Pipeline {} is running".format(self._pipeline_id))
        while self._running.is_set():
            changed = self._update()
            
            self._actions_states["id"] = self._pipeline_id
            self._actions_states["states"] = [a.get_states() for a in self._pipeline]
            if changed == False:
                time.sleep(0.25)
        self._finish()
        self._log.info("Pipeline {} is stopped".format(self._pipeline_id))

    def create_parallel(self, pipeline_id, actions):

        # it is mandatory to ignore sigint since the main thread must manage it.
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)

        self._running.set()
        self._process = multiprocessing.Process(target=PipelineMP._process_kernel, args=(self, pipeline_id, actions))
        self._process.start()

        # restore signal handling
        signal.signal(signal.SIGINT, original_sigint_handler)

    def _connect_actions(self):
        """
        chain each action to the next one
        """
        for action, action_next in zip(self._pipeline[0:-1], self._pipeline[1:]):
            action.set_next(action_next)

    def _update(self):
        for action in self._pipeline:
            try:
                action.update()
            except Exception as e:
                self._log.warning("action {} failed to update ({})".format(action.__class__.__name__, repr(e)))

        return self._is_changed()

    def _finish(self):

        for action in self._pipeline:
            try:
                action.finish()
            except Exception as e:
                self._log.warning("action {} failed to finish ({})".format(action.__class__.__name__, repr(e)))
        
    def finish(self):
        self._running.clear()
        self._process.join()
        self._log.info("Join process done")

    def get_states(self):
        return self._actions_states["id"], self._actions_states["states"]

    def _is_changed(self):
        # return True if something happens in actions since last update
        output = False

        for a in self._pipeline:
            output |= a.get_changed()
            a.reset_changed()

        return output