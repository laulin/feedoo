from feedo.action_change import ActionChange
from feedo.event import Event
import time
import unittest
import os


TEST_DB = "/tmp/test.json"
class TestActionChange(unittest.TestCase):
    def setUp(self):
        try:
            os.remove(TEST_DB)
        except:
            pass

    def test_no_change(self):
        action = ActionChange("*", "alert.change", {"title":"something changed !"}, "c_key", "q_key")
        event = Event("my_tag", 123456789, {"q_key": "XXXX", "c_key":True})
        action.do(event)
        event = Event("my_tag", 123456790, {"q_key": "XXXX", "c_key":True})
        result = action.do(event)

        self.assertEqual(result, event)

    def test_change(self):
        action = ActionChange("*", "alert.change", {"title":"something changed !"}, "c_key", "q_key")
        event = Event("my_tag", 123456789, {"q_key": "XXXX", "c_key":True})
        action.do(event)
        event = Event("my_tag", 123456790, {"q_key": "XXXX", "c_key":False})
        result = action.do(event)

        self.assertEqual(result[1].tag, "alert.change")

    def test_change_not_ignore_null(self):
        action = ActionChange("*", "alert.change", {"title":"something changed !"}, "c_key", "q_key", ignore_null=False)
        event = Event("my_tag", 123456789, {"q_key": "XXXX", "c_key":True})
        action.do(event)
        event = Event("my_tag", 123456790, {"q_key": "XXXX"})
        result = action.do(event)
        
        self.assertEqual(result[1].tag, "alert.change")

    def test_change_ignore_query_key(self):
        action = ActionChange("*", "alert.change", {"title":"something changed !"}, "c_key", "q_key")
        event = Event("my_tag", 123456789, {"c_key":True}) # missing q_key, ignored
        action.do(event)
        event = Event("my_tag", 123456790, {"q_key": "XXXX", "c_key":False})
        result = action.do(event)
        
        self.assertEqual(result, event)

    def test_store_and_load(self):
        old_action = ActionChange("*", "alert.change", {"title":"something changed !"}, "c_key", "q_key", db_path=TEST_DB)
        event = Event("my_tag", 123456789, {"q_key": "XXXX", "c_key":True})
        old_action.do(event)
        old_action.update()

        action = ActionChange("*", "alert.change", {"title":"something changed !"}, "c_key", "q_key", db_path=TEST_DB)
        event = Event("my_tag", 123456790, {"q_key": "XXXX", "c_key":False})
        result = action.do(event)

        self.assertEqual(result[1].tag, "alert.change")