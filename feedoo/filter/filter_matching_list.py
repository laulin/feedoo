from chronyk import Chronyk
from feedoo.abstract_action import AbstractAction
from feedoo.event import Event
import ahocorasick
import time


class FilterMatchingList(AbstractAction):
    def __init__(self, match:str, tag:str, key:str, alert:dict, mode:str="present", matching_list:list=None, matching_list_file:str=None):
        AbstractAction.__init__(self, match)
        self._key = key
        self._tag = tag
        self._alert = alert

        if matching_list is None and matching_list_file is None:
            raise Exception("matching_list or matching_list_file have to be set")
        if matching_list is not None and matching_list_file is not None:
            raise Exception("matching_list and matching_list_file can be set both")
        if mode not in ["present", "absent"]:
            raise Exception("mode value ({}) is in valid, expect 'present' or 'absent'".format(mode))

        self._mode = mode
        if matching_list_file is not None: 
            matching_list = self.load_list(matching_list_file)
        self._automaton = self.build_automaton(matching_list)
        
    def load_list(self, file_name:str):
        self._log.info("load list from file {}".format(file_name))
        with open(file_name) as f:
            return [l.strip() for l in f]

    def build_automaton(self, matching_list:list):
        self._log.info("create aho corasick structure with {} entries".format(len(matching_list)))
        automaton = ahocorasick.Automaton()

        for element in matching_list:
            automaton.add_word(element, element)

        automaton.make_automaton()
        return automaton

    def do(self, event:object, _time=time.time):

        if self._key in event.record:
            value = str(event.record[self._key])
            matching_word = self._automaton.iter(value)
            found = [key for _, key in matching_word]

            if (len(found) == 0 and self._mode == "absent") or (len(found) != 0 and self._mode == "present"):
                found_string = ['"{}"'.format(f) for f in found]
                timestamp = int(_time())
                new_record = {
                    "timestamp" : timestamp,
                    "mode" : self._mode,
                    "found" : ",".join(found_string),
                    "key" : self._key,
                    "value" : value
                }

                new_record.update(self._alert)
                new_event = Event(self._tag, timestamp, new_record)            

                return [event, new_event]

        return Event(event.tag, event.timestamp, event.record)






