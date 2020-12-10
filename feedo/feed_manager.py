from feedo.pipeline import Pipeline
from feedo.plugins import Plugins
import time
import sys
import logging

class FeedManager:
    def __init__(self, configuration):
        self._configuration = configuration
        self._pipelines = []
        self._log = logging.getLogger(str(self.__class__.__name__))

    def setup(self):
        plugins = Plugins()
        action_modules = plugins.load_vanilla()
        for pipeline_id, pipeline_actions in self._configuration.iterate_pipelines():
            self._log.info("Create pipeline {}".format(pipeline_id))
            new_pipeline = Pipeline(action_modules)
            new_pipeline.create(pipeline_actions)

            self._pipelines.append(new_pipeline)

    def update(self):
        for p in self._pipelines:
            p.update()

    def finish(self):
        self._log.debug("Call finish()")
        for p in self._pipelines:
            p.finish()

    def loop(self):
        try:
            self._log.debug("Start processing")
            while(1):
                self.update()
                time.sleep(0.25)
        except KeyboardInterrupt:
            self.finish()
            sys.exit(0)
