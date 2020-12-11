from feedoo.time_frame import TimeFrame
import time
import unittest

class TestTimeFrame(unittest.TestCase):
    def test_add(self):
        tf = TimeFrame(60)
        event = {"data":"xxxx"}
        tf.add_event(event)

        self.assertEqual(len(tf), 1)

    def test_timout(self):
        tf = TimeFrame(60)

        def my_time(dt):
            def t():
                return time.time() + dt
            return t

        event = {"data":"xxxx"}
        tf.add_event(event)

        event2 = {"data":"yyyy"}
        tf.add_event(event2, my_time(3600))

        self.assertEqual(len(tf), 1)