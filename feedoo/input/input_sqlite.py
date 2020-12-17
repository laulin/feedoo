from feedoo.abstract_input_db import AbstractInputDB 
from feedoo.sqlite_adapter import SqliteAdapter

class InputSqlite(AbstractInputDB):

    def __init__(self, tag:str, window:int, time_key:str, table_name_match:str, filename:str, fields:dict, offset:int=0, remove=False, reload_position=False, db_path=None):
        AbstractInputDB.__init__(self, tag, window, time_key, table_name_match, offset, remove, reload_position, db_path)
        self._database_adapter = SqliteAdapter(filename, fields)