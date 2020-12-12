from feedoo.abstract_action import AbstractAction
import time
from feedoo.hash_storage import HashStorage
from feedoo.event import Event

# This action will monitor a certain field and match if that field changes. The field must change with respect to the last event with the same query_key.

class FilterChange(AbstractAction):
    def __init__(self, match, tag, alert, compare_key, query_key, ignore_null=True, db_path=None, timeout=60):
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

        self._state = HashStorage(db_path, timeout)

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
