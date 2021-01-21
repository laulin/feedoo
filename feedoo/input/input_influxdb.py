from feedoo.abstract_action import AbstractAction
from feedoo.event import Event
from influxdb import InfluxDBClient
import time


class InputInfluxdb(AbstractAction):
    def __init__(self, tag:str, query:str, window:int=60, initial_query:str=None, database:str="telegrag", host:str="localhost", port:int=8086):
        AbstractAction.__init__(self)
        self._query = query
        self._initial_query = initial_query
        self._client = InfluxDBClient(host=host, port=port, database=database)
        self._window = int(window)
        self._last_time = time.time()
    
    def do(self, event):
        # directly forward
        return event

    def push_results(self, results):
        for document in results.get_points():
            event = Event(self._tag, int(time.time()), document)
            self.call_next(event)

    def update(self):
        if self._initial_query is not None:
            results = self._client.query(self._initial_query)
            self._initial_query = None
            self.push_results(results)
        else:
            if time.time() - self._last_time >= self._window:
                results = self._client.query(self._query)
                self.push_results(results)
                self._last_time = time.time()
        

                

            
                