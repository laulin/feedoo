from feedo.output.output_stdout import OutputStdout
from feedo.event import Event
import unittest


class TestOutputStdout(unittest.TestCase):
    def test_1(self):
        e = Event("my_tag", 123456789, '{"field":"test_1"}')
        action = OutputStdout("*")
        action.receive(e)
