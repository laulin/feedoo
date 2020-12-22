from feedoo.filter.filter_matching_list import FilterMatchingList
from feedoo.event import Event
import unittest
import os

def my_time(dt):
    def t():
        return dt
    return t


class TestFilterMatchingList(unittest.TestCase):
    def test_from_list(self):
        FilterMatchingList(match="*", 
                            tag="alert.bl", 
                            key="field_1", 
                            alert={"title": "alert !"}, 
                            mode="present", 
                            matching_list=["aaaaa", "bbbbb", "ccccc"])

    def test_from_file(self):
        FilterMatchingList(match="*", 
                            tag="alert.bl", 
                            key="field_1", 
                            alert={"title": "alert !"}, 
                            mode="present", 
                            matching_list_file="/root/tests/list.txt")
    
    def test_darklist(self):
        fml = FilterMatchingList(match="*", 
                            tag="alert.bl", 
                            key="field_1", 
                            alert={"title": "alert !"}, 
                            mode="present", 
                            matching_list=["aaaaa", "bbbbb", "ccccc"])

        event = Event("data", 123456789, {"field_1":"test aaaaah !"})
        events = fml.do(event, my_time(0))
        result = events[1].record
   
        expected = {'timestamp': 0, 'mode': 'present', 'found': '"aaaaa"', 'key': 'field_1', 'value': 'test aaaaah !', 'title': 'alert !'}
        
        self.assertEqual(result, expected)

    def test_lightlist(self):
        fml = FilterMatchingList(match="*", 
                            tag="alert.bl", 
                            key="field_1", 
                            alert={"title": "alert !"}, 
                            mode="absent", 
                            matching_list=["aaaaa", "bbbbb", "ccccc"])

        event = Event("data", 123456789, {"field_1":"test dddddh !"})
        events = fml.do(event, my_time(0))
        result = events[1].record
   
        expected = {'timestamp': 0, 'mode': 'absent', 'found': '', 'key': 'field_1', 'value': 'test dddddh !', 'title': 'alert !'}
        
        self.assertEqual(result, expected)

    def test_darklist_from_file(self):
        fml = FilterMatchingList(match="*", 
                            tag="alert.bl", 
                            key="field_1", 
                            alert={"title": "alert !"}, 
                            mode="present", 
                            matching_list_file="/root/tests/list.txt")

        event = Event("data", 123456789, {"field_1":"test aaaaah !"})
        events = fml.do(event, my_time(0))
        result = events[1].record
   
        expected = {'timestamp': 0, 'mode': 'present', 'found': '"aaaaa"', 'key': 'field_1', 'value': 'test aaaaah !', 'title': 'alert !'}
        
        self.assertEqual(result, expected)




