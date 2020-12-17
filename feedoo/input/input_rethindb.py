from feedoo.abstract_input_db import AbstractInputDB 
from feedoo.rethinkdb_adapter import RethinkdbAdapter

class InputRethinkdb(AbstractInputDB):

    def __init__(self, tag:str, window:int, table_name_match:str, timestamp_index:str, ip:str="localhost", port:int=28015, database_name:str="test", wait_connection:int=30, offset:int=0, remove:bool=False, reload_position:bool=False, db_path:str=None):
        AbstractInputDB.__init__(self, tag, window, timestamp_index, table_name_match, offset, remove, reload_position, db_path)
        self._database_adapter = RethinkdbAdapter(ip, port, database_name, wait_connection, timestamp_index)