import sqlite3
import logging


class SqliteAdapter:
    def __init__(self, filename:str, fields:dict):
        self._filename = filename
        self._fields = fields
        self._field_names = sorted(self._fields.keys())
        self._connection = None
        self._log = logging.getLogger("SqliteAdapter")

    def connect(self):
        self._connection = sqlite3.connect(self._filename)

    def close(self):
        self._connection.close()

    def create_table_unique(self, table_name:str):
        cursor = self._connection.cursor()
        fields = []
        for name, field_type in self._fields.items():
            tmp = "{} {}".format(name, field_type.upper())
            fields.append(tmp)

        sql_cmd = "CREATE TABLE IF NOT EXISTS {} ({});".format(table_name, ",".join(fields))
        self._log.debug("Execute : " + sql_cmd)

        cursor.execute(sql_cmd)
        self._connection.commit()

    def _prepare_data(self, document):
        output = list()
        for k in self._field_names:
            field = document[k]
            if isinstance(field, str):
                output.append("{}".format(field))
            else:
                output.append("{}".format(field))
        return output

    def insert_bulk(self, table_name:str, documents:list):
        field_names = set(self._field_names)
        sql_cmd = "INSERT INTO {} ({}) VALUES ({})".format(table_name, ",".join(self._field_names), ",".join(["?"] * len(self._field_names)))
        self._log.debug("Insert command : " + sql_cmd)

        cursor = self._connection.cursor()
        for document in documents:
            if field_names.intersection(document) != field_names:
                self._log.debug("Document not inserted (fields are not compliant) : '{}'".format(document))
            else:
                fields = self._prepare_data(document)

                cursor.execute(sql_cmd, fields)
        self._connection.commit()

    def get_time_serie(self, table_name:str, time_field:str, from_timestamp:int, to_timestamp:int):
        context = {
            "fields" : ", ".join(self._field_names),
            "table" : table_name,
            "ts" : time_field,
            "min" : int(from_timestamp),
            "max" : int(to_timestamp)
        }
        sql_cmd = "SELECT {fields} FROM {table} WHERE {ts} >= {min} AND {ts} < {max} ORDER BY {ts}".format(**context)
        self._log.debug("Select command : " + sql_cmd)

        cursor = self._connection.cursor()
        cursor.execute(sql_cmd)

        output = [dict(zip(self._field_names, v)) for v in cursor.fetchall()]
        return output


    