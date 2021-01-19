from feedoo.abstract_action import AbstractAction
from feedoo.event import Event

from fluentbit_server.fluentbit_authentication import FluentbitAuthentication
from fluentbit_server.fluentbit_transport import FluentbitTransport
from fluentbit_server.fluentbit_request_handler import FluentbitRequestHandler
from fluentbit_server.fluentbit_server import FluentbitServer
from fluentbit_server.fluentbit_ssl import FluentbitSSL
from functools import partial
import threading
import queue

class InputForward(AbstractAction):
    def __init__(self, host="localhost", port=24224, tls_enable=False, key_file=None, crt_file=None, shared_key=None, server_hostname="", buffer_size=32768, queue_size=1000, _start_server=True):
        AbstractAction.__init__(self)
        transport_factory = partial(FluentbitTransport, callback=self.callback, buffer_size=buffer_size)

        if shared_key is not None:
             authentication_factory = partial(FluentbitAuthentication, shared_key=shared_key, server_hostname=server_hostname)
        else:
            authentication_factory = None

        if tls_enable:
            ssl = FluentbitSSL(key_file=key_file, crt_file=crt_file)
        else:
            ssl = None

        self._queue = queue.Queue(queue_size)
        self._server = None
        if _start_server:
            self._server = FluentbitServer((host, port), FluentbitRequestHandler, transport_factory, authentication_factory, ssl)
            self._thread = threading.Thread(target=self._server.serve_forever)
            self._thread.start()

    def callback(self, event):
        try:
            self._queue.put(event)
            self._log.debug("Forward received event {}".format(event))
        except queue.Full:
            self._log.warning("Queue is full, drop event")

    def do(self, event):
        return event

    def format_record(self, record):
        output = dict()

        for k, v in record.items():
            try:
                new_k = k.decode("utf8")
            except Exception as e:
                new_k = k

            try:
                new_v = v.decode("utf8")
            except:
                new_v = v

            output[new_k] = new_v
        return output

    def _update_one_event(self):
        event = self._queue.get_nowait()
        record = self.format_record(event[2])
        new_event = Event(event[0].decode("utf8"), event[1], record)
        self.call_next(new_event)

    def update(self):
        for i in range(16):
            try:
                self._update_one_event()
            except queue.Empty:
                return

    def finish(self):
        self._log.info("Shutdown the server")
        if self._server is not None:
            self._server.shutdown()
        self._log.info("Purge the queue")

        while(1):
            try:
                self._update_one_event()
            except queue.Empty:
                return

