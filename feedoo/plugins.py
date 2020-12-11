import pkgutil
import logging

import feedoo.input
import feedoo.output
import feedoo.filter
import feedoo.parser


class Plugins:
    def __init__(self):
        self._log = logging.getLogger("Plugins")

    def camel_format(self, w):
        return w[0].upper() + "".join([y.lower() for y in w[1:]])

    def snake_to_camel_case(self, name):
        words = name.split("_")
        tmp = map(self.camel_format , words)
        return "".join(tmp)

    def load_from_package(self, package, prefix=""):
        # This function search all module in a package that start with a prefix
        # and it returns a dict with module name/associated object in CamelCase
        output = {}
        self._log.info("Walk package {}".format(package.__name__))
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
            if ispkg == False and modname.startswith(prefix):
                self._log.info("Found module {}".format(modname))
                module = importer.find_module(modname).load_module(modname)
                output[modname] = getattr(module, self.snake_to_camel_case(modname))

        return output

    def load_vanilla(self):
        # load all packages related to feedoo processing
        packages = {
            feedoo.input : "input_",
            feedoo.output : "output_",
            feedoo.parser : "parser_",
            feedoo.filter : "filter_"
        }
        output = {}
        for package, prefix in packages.items():
            self._log.info("Load package {} with prefix {}".format(package.__name__, prefix))
            tmp = self.load_from_package(package, prefix)
            self._log.info("Loaded : {}".format(tmp))
            output.update(tmp)

        return output
