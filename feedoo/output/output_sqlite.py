from feedoo.abstract_output_db import AbstractOutputDB 
from feedoo.sqlite_adapter import SqliteAdapter

class OutputSqlite(AbstractOutputDB):

    def __init__(self, match:str, time_key:str, table_template:str, filename:str, fields:dict, buffer_size:int=1000, timeout_flush:int=60, db_path:str=None):
        AbstractOutputDB.__init__(self, match, time_key, table_template, buffer_size, timeout_flush, db_path)
        self._database_adapter = SqliteAdapter(filename, fields)