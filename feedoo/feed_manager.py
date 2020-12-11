from feedoo.pipeline import Pipeline
from feedoo.plugins import Plugins
import time
import sys
import logging
import os
import pwd
import grp

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

    def _get_uid(self):
        uid = os.getuid()
        gid = os.getgid()

        uid_name = pwd.getpwuid(uid)[0]
        gid_name = grp.getgrgid(gid)[0]

        self._log.info('Run as uid:{} gid:{}'.format(uid_name, gid_name))
        
        return uid, gid

    def _name_to_id(self, uid_name, gid_name):
            # Get the uid/gid from the name
            uid = pwd.getpwnam(uid_name)[2]
            gid = grp.getgrnam(gid_name)[2]

            return uid, gid

    def _drop_gid(self, runtime_gid):
        try:
            os.setgid(runtime_gid)
        except OSError as e:
            self._log.error('Could not set effective group id: {}'.format(repr(e)))

    def _drop_uid(self, runtime_uid):
        try:
            os.setuid(runtime_uid)
        except OSError as e:
            self._log.error('Could not set effective user id: {}'.format(repr(e)))

    def drop_privileges(self):
        # thank to :
        #   http://antonym.org/2005/12/dropping-privileges-in-python.html
        #   https://stackoverflow.com/questions/2699907/dropping-root-permissions-in-python
        uid_name,  gid_name = self._configuration.get_privileges()
        starting_uid, _ = self._get_uid()
        
        if starting_uid != 0:
            self._log.info("Not root, nothing to drop")
            return

        if uid_name is None:
            if starting_uid == 0:
                self._log.warning("You will remain as root - I'm sure you know it's dangerous !")
            else:
                self._log.info("Not privileges drop")
            return

        # If we started as root, drop privs and become the specified user/group
        if starting_uid == 0:

            running_uid, running_gid = self._name_to_id(uid_name, gid_name)
            self._drop_gid(running_gid)
            self._drop_uid(running_uid)

            # Ensure a very convervative umask
            new_umask = 0o77
            old_umask = os.umask(new_umask)
            self._log.info('drop_privileges: Old umask: {}, new umask: {}'.format(oct(old_umask), oct(new_umask)))

        self._get_uid()

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
