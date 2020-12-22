from feedoo.feedoo_states import StatesServer
from feedoo.feedoo_states import FeedooStates

import unittest
import time
import threading
import urllib.request

class TestFeedooStates(unittest.TestCase):
    def test_1(self):
        def callback():
            return {"timestamp":123456, "pipelines":{}}

        server = StatesServer("127.0.0.1", 4321, callback)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()

        server.shutdown()

    def test_2(self):
        def callback():
            return {"timestamp":123456, "pipelines":{}}

        server = StatesServer("127.0.0.1", 4321, callback)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        result = urllib.request.urlopen("http://127.0.0.1:4321").read()
        expected = b'{\n    "pipelines": {},\n    "timestamp": 123456\n}'
        server.shutdown()

        self.assertEqual(result, expected)

    def test_3(self):
        def callback():
            return {"timestamp":123456, "pipelines":{}}

        server = FeedooStates("127.0.0.1", 4321, callback)

        result = urllib.request.urlopen("http://127.0.0.1:4321").read()
        expected = b'{\n    "pipelines": {},\n    "timestamp": 123456\n}'
        server.finish()

        self.assertEqual(result, expected)



