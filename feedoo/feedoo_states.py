import http.server
import json
import threading
import logging

class StatesHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"")
        else:
            self.send_response(200)
            self.end_headers()
            states = self.server.callback()
            payload = json.dumps(states, sort_keys=True, indent=4)
            self.wfile.write(payload.encode("utf8"))

class StatesServer(http.server.ThreadingHTTPServer):
    allow_reuse_address = True
    def __init__(self, ip:str, port:int, callback:object):
        http.server.ThreadingHTTPServer.__init__(self, (ip, port), StatesHandler)
        self.callback = callback

class FeedooStates:
    def __init__(self, ip:str, port:int, callback:object):
        self._ip = ip
        self._port = port
        self._server = None
        self._thread = None
        self._log = logging.getLogger("FeedooStates")

        if ip is not None and port is not None:
            self._log.info("Create server http://{}:{}/ ".format(ip, port))
            if ip not in ["", "localhost", "127.0.0.1"]:
                self._log.warning("The HTTP server should not be exposed outside the loopback. DO NOT EXPOSE ON INTERNET !")
            self._server = StatesServer("127.0.0.1", 4321, callback)
            self._thread = threading.Thread(target=self._server.serve_forever)
            self._thread.start()

    def finish(self):
        if self._server is not None:
            self._log.info("Stop http server")
            self._server.shutdown()