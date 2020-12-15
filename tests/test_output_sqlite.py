from feedoo.output.output_sqlite import OutputSqlite
from feedoo.event import Event
import unittest
from time import time

FIELDS = {"timestamp":"INTEGER", "name":"TEXT", "age":"INTEGER"}
class TestOutputSqlite(unittest.TestCase):
    def test_init(self):
        output_sqlite = OutputSqlite("*", "timestamp", "table_%Y%m%d", ":memory:", FIELDS)