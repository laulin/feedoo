import yaml
import pprint
import logging
from glob import glob
import string

def loader(filename):
    with open(filename) as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)

    return data


class FormatDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"

class Configuration:
    def __init__(self):
        self._structure = {}
        self._log = logging.getLogger("Configuration")

    def load(self, filename, _loader=loader):
        self._structure = _loader(filename)
        self._structure["pipelines"] = self._structure.get("pipelines", {})
        self._structure["variables"] = self._structure.get("variables", {})
        self.include_pipelines(_loader)
        self._log.debug("variables : {} ".format(pprint.pformat(self._structure["variables"]) ))
        self._structure["pipelines"] = self.interpolate(self._structure["pipelines"], self._structure["variables"])

    def include_pipelines(self, _loader=loader):
        if self._structure.get("include") is not None:
            paths = list(glob(self._structure["include"]))
            for path in paths:
                self._log.debug("include {}".format(path))
                self._structure["pipelines"][path] = _loader(path)
            if len(paths) == 0:
                self._log.warning("{} doesn't match any file".format(self._structure["include"]))
        else:
            self._log.debug("no include path")
        
    def iterate_pipelines(self):

        for pipeline_id, pipeline in self._structure["pipelines"].items():
            self._log.debug("pipeline of {} : {} ".format(pipeline_id, pprint.pformat(pipeline) ))

            yield (pipeline_id, pipeline)

    def interpolate(self, input_structure, variables):

        if isinstance(input_structure, dict):
            input_structure = dict(input_structure)
            for k, v in input_structure.items():
                input_structure[k] = self.interpolate(v, variables)

        elif isinstance(input_structure, list):
            input_structure = list(input_structure)
            for i,v in enumerate(input_structure):
                input_structure[i] = self.interpolate(v, variables)

        elif isinstance(input_structure, str):
            try:
                fd = FormatDict(variables)
                formatter = string.Formatter()
                input_structure = formatter.vformat(input_structure, (), fd)
            except Exception as e:
                self._log.info("Fail to interpolate '{}' ({})".format(input_structure, e))

        return input_structure

    def get_privileges(self):
        if "privileges" in self._structure and "user" in self._structure["privileges"] and "group" in self._structure["privileges"]:
            return self._structure["privileges"]["user"], self._structure["privileges"]["group"]
        else:
            return None, None
