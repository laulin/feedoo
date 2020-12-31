import logging
from pprint import pprint
import multiprocessing
import time
import signal

def _parallel_pipeline(this, pipeline_id, actions):
    this.create(pipeline_id, actions)

    this._log.info("Pipeline {} is running".format(this._pipeline_id))
    while this._running.is_set():
        changed = this.update()
        if changed == False:
            time.sleep(0.25)
    this._finish()
    this._log.info("Pipeline {} is stopped".format(this._pipeline_id))

class Pipeline:
    def __init__(self, actions):
        self._log = logging.getLogger("Pipeline")
        self._pipeline = []
        self._actions = actions
        self._pipeline_id = None
        self._running = None
        self._process = None

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
        self.connect_actions()

    def create_parallel(self, pipeline_id, actions):

        # it is mandatory to ignore sigint since the main thread must manage it.
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)

        self._running = multiprocessing.Event()
        self._running.set()
        self._process = multiprocessing.Process(target=_parallel_pipeline, args=(self, pipeline_id, actions))
        self._process.start()

        # restore signal handling
        signal.signal(signal.SIGINT, original_sigint_handler)

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
                self._log.warning("action {} failed to update ({})".format(action.__class__.__name__, repr(e)))

        return self._is_changed()

    def _finish(self):

        for action in self._pipeline:
            try:
                action.finish()
            except Exception as e:
                self._log.warning("action {} failed to finish ({})".format(action.__class__.__name__, repr(e)))
        
    def finish(self):
        if self._running is not None:
            self._running.clear()
            self._process.join()
            self._log.info("Join process done")

    def get_states(self):
        return self._pipeline_id, [a.get_states() for a in self._pipeline]

    def _is_changed(self):
        # return True if something happens in actions since last update
        output = False

        for a in self._pipeline:
            output |= a.get_changed()
            a.reset_changed()

        return output