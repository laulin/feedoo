from rethinkdb import r as Rethinkdb
import logging
import time


class RethinkdbAdapter:
    def __init__(self, ip:str="localhost", port:int=28015, database_name:str="test", wait_connection:int=30, timestamp_index="timestamp"):
        self._ip = ip
        self._port = int(port)
        self._database_name = database_name
        self._wait_connection = wait_connection
        self._connection = None
        self._timestamp_index = timestamp_index
        self._log = logging.getLogger("RethinkDBAdapter")


    def is_connected(self):
        return self._connection is not None

    def connect(self):
        counter = self._wait_connection

        while True:
            try:
                self._connection = Rethinkdb.connect(self._ip, self._port)
                self._is_connected = True
                return
            except Exception as e:
                time.sleep(1)
                counter = counter -1

                if counter <= 0:
                    self._log.warning("Can't establish connection on {}:{}".format(self._ip, self._port))
                    raise e 
            except rethinkdb.errors.ReqlTimeoutError as e:
                self._log.warning("request timeout on {}:{}".format(self._ip, self._port))
        

    def close(self):
        self._connection.close()
        self._connection = None

    def create_table_unique(self, table_name:str):
        tables = Rethinkdb.db(self._database_name).table_list().run(self._connection)

        if table_name not in tables:
            Rethinkdb.db(self._database_name).table_create(table_name).run(self._connection)
            
            self._log.info("create table "+table_name)

    def delete_table(self, table_name:str):
        if table_name in self.list_tables():
            Rethinkdb.db(self._database_name).table_drop(table_name).run(self._connection)

    def insert_bulk(self, table_name:str, documents:list):
        Rethinkdb.db(self._database_name).table(table_name).index_wait().run(self._connection)
        Rethinkdb.db(self._database_name).table(table_name).insert(documents).run(self._connection)
        if self._timestamp_index not in Rethinkdb.table(table_name).index_list().run(self._connection):
            Rethinkdb.db(self._database_name).table(table_name).index_create(self._timestamp_index).run(self._connection)
            Rethinkdb.db(self._database_name).table(table_name).index_wait(self._timestamp_index).run(self._connection)


    def get_time_serie(self, table_name:str, time_field:str, from_timestamp:int, to_timestamp:int):
        Rethinkdb.db(self._database_name).table(table_name).index_wait().run(self._connection)
        return list(Rethinkdb.db(self._database_name).table(table_name).between(from_timestamp, to_timestamp, index=time_field, right_bound="closed").without("id").order_by(time_field).run(self._connection))

    def list_tables(self):
        tables = list(Rethinkdb.db(self._database_name).table_list().run(self._connection))

        return tables

    def is_table_empty(self, table_name):
        counter = Rethinkdb.db(self._database_name).table(table_name).limit(1).count().run(self._connection)

        if counter == 0:
            return True
        else:
            return False

    def get_max(self, table_name, field):
        tmp = Rethinkdb.db(self._database_name).table(table_name).max(field).pluck(field).run(self._connection)
        return tmp[field]

    def get_min(self, table_name, field):
        tmp = Rethinkdb.db(self._database_name).table(table_name).min(field).pluck(field).run(self._connection)
        return tmp[field]


    def delete_time_serie(self, table_name:str, time_field:str, from_timestamp:int, to_timestamp:int):
        Rethinkdb.db(self._database_name).table(table_name).index_wait().run(self._connection)
        return list(Rethinkdb.db(self._database_name).table(table_name).between(from_timestamp, to_timestamp, index=time_field, right_bound="closed").delete().run(self._connection))



    