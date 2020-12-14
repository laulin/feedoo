from feedoo.time_frame import TimeFrame
import time
import unittest

def my_time(dt):
    def t():
        return time.time() + dt
    return t

class TestTimeFrame(unittest.TestCase):
    def test_add(self):
        tf = TimeFrame(60)
        event = {"data":"xxxx"}
        tf.add_event(event)

        self.assertEqual(len(tf), 1)

    def test_timout(self):
        tf = TimeFrame(60)

        event = {"data":"xxxx"}
        tf.add_event(event)

        event2 = {"data":"yyyy"}
        tf.add_event(event2, _time=my_time(3600))

        self.assertEqual(len(tf), 1)

    def test_average(self):
        tf = TimeFrame(60)
        tf.add_event(1)
        tf.add_event(3)
        result = tf.average()
        expected = 2

        self.assertEqual(result, expected)

    def test_next_1(self):
        tf2 = TimeFrame(120)
        tf = TimeFrame(60, tf2)

        tf.add_event(1, _time=my_time(0))
        tf.add_event(3, _time=my_time(70))
        result = tf.add_event(4, _time=my_time(130))
        expected = 1

        self.assertEqual(result[0][1], expected)