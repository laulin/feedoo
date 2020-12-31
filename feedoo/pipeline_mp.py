import logging
from pprint import pprint
import multiprocessing
import time
import signal
from feedoo.pipeline_sp import PipelineSP

class PipelineMP:
    def __init__(self, actions):
        self._log = logging.getLogger("PipelineMP")
        self._pipeline_sp = PipelineSP(actions)
        self._running = multiprocessing.Event()
        self._process = None
        self._manager = multiprocessing.Manager()
        self._actions_states = self._manager.dict()

    def _process_kernel(self, pipeline_id, actions):
        self._pipeline_sp.create(pipeline_id, actions)

        self._actions_states["id"] = pipeline_id
        self._log.info("Pipeline {} is running".format(pipeline_id))
        while self._running.is_set():
            changed = self._pipeline_sp.update()
            
            _, self._actions_states["states"] = self._pipeline_sp.get_states()
            if changed == False:
                time.sleep(0.25)
        self._pipeline_sp.finish()
        self._log.info("Pipeline {} is stopped".format(pipeline_id))

    def create(self, pipeline_id, actions):

        # it is mandatory to ignore sigint since the main thread must manage it.
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)

        self._running.set()
        self._process = multiprocessing.Process(target=PipelineMP._process_kernel, args=(self, pipeline_id, actions))
        self._process.start()

        # restore signal handling
        signal.signal(signal.SIGINT, original_sigint_handler)

    def update(self):
        pass

    def finish(self):
        self._running.clear()
        self._process.join()
        self._log.info("Join process done")

    def get_states(self):
        return self._actions_states["id"], self._actions_states["states"]