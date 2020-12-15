from feedoo.abstract_output_db import AbstractOutputDB 
from feedoo.rethinkdb_adapter import RethinkdbAdapter

class OutputRethinkdb(AbstractOutputDB):

    def __init__(self, match:str, timestamp_index:str, table_template:str, ip:str="localhost", port:int=28015, database_name:str="test", wait_connection:int=30, buffer_size:int=1000, timeout_flush:int=60, db_path:str=None):
        AbstractOutputDB.__init__(self, match, timestamp_index, table_template, buffer_size, timeout_flush, db_path)
        self._database_adapter = RethinkdbAdapter(ip, port, database_name, wait_connection, timestamp_index)