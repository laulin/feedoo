from feedoo.pipeline_mp import PipelineMP
from feedoo.plugins import Plugins
from feedoo.feedoo_states import FeedooStates
from feedoo.privileges import Privileges
import time
import sys
import logging


class FeedManager:
    def __init__(self, configuration):
        self._configuration = configuration
        self._pipelines = []
        self._log = logging.getLogger(str(self.__class__.__name__))
        self._states = None

    def setup(self):
        plugins = Plugins()
        action_modules = plugins.load_vanilla()
        for pipeline_id, pipeline_actions in self._configuration.iterate_pipelines():
            self._log.info("Create pipeline {}".format(pipeline_id))
            new_pipeline = PipelineMP(action_modules)
            new_pipeline.create(pipeline_id, pipeline_actions)

            self._pipelines.append(new_pipeline)

        self.setup_states()

    def setup_states(self):
        parameters = self._configuration.get_states_parameters()
        parameters["callback"] = self.get_states
        self._states = FeedooStates(**parameters)

    def drop_privileges(self):
        uid_name,  gid_name = self._configuration.get_privileges()
        privileges = Privileges(uid_name,  gid_name)
        privileges.drop_privileges()

    def update(self):
        output = False
        for p in self._pipelines:
            output |= p.update()
        return output

    def finish(self):
        self._log.debug("Call finish()")
        for p in self._pipelines:
            p.finish()
        self._states.finish()

    def loop(self):
        try:
            self._log.debug("Start processing")
            while(1):
                time.sleep(0.25)
        except KeyboardInterrupt:
            self.finish()
            sys.exit(0)

    def get_states(self):
        pipeline_states = dict([p.get_states() for p in self._pipelines])
        timestamp = time.time()

        return {
            "timestamp" : timestamp,
            "pipelines" : pipeline_states
        }
