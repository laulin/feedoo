from feedoo.abstract_output_file import AbstractOutputFile
from chronyk import Chronyk
import json

# push document to file using line protocol

class OutputLineProtocol(AbstractOutputFile):
    def __init__(self, match, time_key, mesurement, tag_keys, field_keys, path_template, buffer_size=1000, timeout_flush=60, db_path=None):
        AbstractOutputFile.__init__(self, match, time_key, path_template, buffer_size, timeout_flush, db_path)

        self._mesurement = mesurement
        self._tag_keys = tag_keys
        self._field_keys = field_keys
        self._header = self.make_header()

    def make_header(self):
        header = self._mesurement

        for tag in self._tag_keys:
            header += "," + tag + "={" + tag + "}"

        self._log.debug("Header : '{}'".format(header))
        return header

    def value_to_string(self, values):
        lines = []
        for v in values:
            try:
                tmp = []

                for f in self._field_keys:
                    value = v[f]
                    if isinstance(value, str):
                        tmp.append('{name}="{value}"'.format(name=f, value=value))
                    else:
                        tmp.append('{name}={value}'.format(name=f, value=value))

                time = Chronyk(v[self._time_key])
                ts = int(time.timestamp() * 1000)
                line = "{} {} {}".format(self._header, ",".join(tmp), ts)
                lines.append(line)
            except Exception as e:
                self._log.warning("failed to create line '{}'".format(repr(e)))

        return "\n".join(lines) + "\n"
