import logging
import unittest
from feedo.input_file import InputFile
from unittest.mock import Mock

class TestInputFile(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.WARNING)

    def test_1(self):
        input_file = InputFile("syslog", "/tmp", "/tmp/*est.log")
        action = Mock()
        input_file.set_next(action)

    def test_2(self):

        input_file = InputFile("syslog", "/tmp", "/tmp/*est.log")
        action = Mock()
        input_file.set_next(action)
        input_file.update()

    def test_3(self):

        input_file = InputFile("syslog", "/tmp", "/tmp/*est.log")
        action = Mock()
        input_file.set_next(action)
        input_file.update()

        with open("/tmp/test.log", "w") as f:
            f.write("test\n")

        input_file.update()

    def test_4(self):

        input_file = InputFile("syslog", "/tmp", "/tmp/*est.log", True)
        action = Mock()
        input_file.set_next(action)
        input_file.update()

        with open("/tmp/test.log", "w") as f:
            f.write("test\n")

        input_file.update()

    def test_5(self):

        input_file = InputFile("syslog", "/tmp", "/tmp/*est.log", True)
        action = Mock()
        input_file.set_next(action)

        with open("/tmp/test.log", "w") as f:
            f.write("test\n")

        input_file.update()