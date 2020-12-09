from feedo.action_stdout import ActionStdout
from feedo.event import Event
import unittest


class TestActionStdout(unittest.TestCase):
    def test_1(self):
        e = Event("my_tag", 123456789, '{"field":"test_1"}')
        action = ActionStdout("*")
        action.receive(e)
