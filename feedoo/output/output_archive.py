from feedoo.abstract_output_file import AbstractOutputFile
import json

# push document to archive files

class OutputArchive(AbstractOutputFile):
    def __init__(self, match, time_key, path_template, buffer_size=1000, timeout_flush=60, db_path=None):
        AbstractOutputFile.__init__(self, match, time_key, path_template, buffer_size, timeout_flush, db_path)

    def value_to_string(self, values):
        return "\n".join(map(json.dumps, values)) + "\n"

