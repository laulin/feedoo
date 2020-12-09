from abstract_action import AbstractAction
from event import Event
import time
import unittest
from hash_storage import HashStorage
import os

# This action will monitor a certain field and match if that field changes. The field must change with respect to the last event with the same query_key.

class ActionChange(AbstractAction):
    def __init__(self, match, tag, alert, compare_key, query_key, ignore_null=True, db_path=None):
        # match defines the pattern to be matched
        # tag is the alert tag
        # alert is a dict used to create alert
        # compare_key defines the key to be compared
        # query_key defines the key used to select event. This field must be present in all of the events that are checked.
        # ignore_null is used to ignore if event doesn't have the field.
        # db_path is used to store internal state in case of reloading
        AbstractAction.__init__(self, match)
        
        self._compare_key = compare_key
        self._query_key = query_key
        self._ignore_null = ignore_null
        self._tag = tag
        self._match = match
        self._alert = alert

        self._state = HashStorage(db_path)
        self._state.load()

    def do(self, event):
        record = event.record
        
        if self._query_key not in record:
            # no valid, ignore
            return event

        query_key = record[self._query_key]
        compare_key = record.get(self._compare_key)
        if compare_key is None and self._ignore_null:
            # ignore non existing key
                        return event

        if self.is_key_present(query_key):
            if self.is_unchanged(query_key, compare_key):
                # no change
                return event
            else:
                # change happened !
                alert_record = dict(self._alert)
                alert_record["timestamp"] = int(time.time())
                alert_record["query_key"] = query_key
                alert_record["old_value"] = self.get(query_key)
                alert_record["new_value"] = compare_key

                self.insert(query_key, compare_key)
                return [event, Event(self._tag, int(time.time()), alert_record)]
        else :
            self.insert(query_key, compare_key)
            return event

    def is_key_present(self, query_key):
        return query_key in self._state
    
    def insert(self, query_key, compare_key):
        self._state[query_key] = compare_key

    def is_unchanged(self, query_key, compare_key):
        return self._state[query_key] == compare_key

    def get(self, query_key):
        return self._state[query_key]

    def update(self):
        self._state.store()



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