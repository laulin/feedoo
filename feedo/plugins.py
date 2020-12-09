import pkgutil
import logging


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
        output = {}
        self._log.info("Walk package {}".format(package.__name__))
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
            if ispkg == False:
                self._log.info("Found module {}".format(modname))
                module = importer.find_module(modname).load_module(modname)
                output[prefix+modname] = getattr(module, self.snake_to_camel_case(modname))

        return output
