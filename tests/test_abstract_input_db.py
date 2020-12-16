from feedoo.abstract_input_db import AbstractInputDB
import unittest
from pprint import pprint

class TestAbstractInputDB(unittest.TestCase):
    def test_1(self):
        abstract_input_db = AbstractInputDB(tag="log", 
                                            windows=60, 
                                            time_key="timestamp", 
                                            table_name_template="log_%Y%m%d", 
                                            table_name_match="log_*", 
                                            offset=0, 
                                            remove=False, 
                                            reload_position=False, 
                                            db_path=None)

    def test_get_matching_table(self):
        abstract_input_db = AbstractInputDB(tag="log", 
                                            windows=60, 
                                            time_key="timestamp", 
                                            table_name_template="log_%Y%m%d", 
                                            table_name_match="log_*", 
                                            offset=0, 
                                            remove=False, 
                                            reload_position=False, 
                                            db_path=None)

        all_tables = ["log_20201215", "sys_20201215"]
        expected = ["log_20201215"]
        result = list(abstract_input_db.get_table_matching(all_tables))

        self.assertEqual(result, expected)

    def test_iterate_time_range_first(self):
        abstract_input_db = AbstractInputDB(tag="log", 
                                            windows=60, 
                                            time_key="timestamp", 
                                            table_name_template="log_%Y%m%d", 
                                            table_name_match="log_*", 
                                            offset=0, 
                                            remove=False, 
                                            reload_position=False, 
                                            db_path=None)

        time_range = [
            ("log_20201214", 1607904000, 1607990399), # dec 14 0h00 à dec 14 23h59:59
            ("log_20201215", 1607990400, 1608076799) # dec 15 0h00 à dec 15 23h59:59
        ]

        ranges = [x for x in abstract_input_db.iterate_time_range(time_range, 1607817600, 1608055200)] # dec 13 0h00 to dec 15 18h00
        result = ranges[0]
        expected = ('log_20201214', 1607904000, 1607904059)

        self.assertEqual(result, expected)

    def test_iterate_time_range_last(self):
        abstract_input_db = AbstractInputDB(tag="log", 
                                            windows=60, 
                                            time_key="timestamp", 
                                            table_name_template="log_%Y%m%d", 
                                            table_name_match="log_*", 
                                            offset=0, 
                                            remove=False, 
                                            reload_position=False, 
                                            db_path=None)

        time_range = [
            ("log_20201214", 1607904000, 1607990399), # dec 14 0h00 à dec 14 23h59:59
            ("log_20201215", 1607990400, 1608076799) # dec 15 0h00 à dec 15 23h59:59
        ]

        ranges = [x for x in abstract_input_db.iterate_time_range(time_range, 1607817600, 1608055200)] # dec 13 0h00 to dec 15 18h00
        result = ranges[-1]
        expected = ('log_20201215', 1608055140, 1608055199)

        self.assertEqual(result, expected)

    def test_iterate_time_range_window_bigger_than_data(self):
        abstract_input_db = AbstractInputDB(tag="log", 
                                            windows=60, 
                                            time_key="timestamp", 
                                            table_name_template="log_%Y%m%d", 
                                            table_name_match="log_*", 
                                            offset=0, 
                                            remove=False, 
                                            reload_position=False, 
                                            db_path=None)

        time_range = [
            ("log_20201214", 1607904010, 1607904050), # dec 14 0h00:10 à dec 14 00h00:50
        ]

        ranges = [x for x in abstract_input_db.iterate_time_range(time_range, 1607904000, 1607904060)] # dec 14 0h00:00 à dec 14 00h01:00
        result = ranges[0]
        expected = ("log_20201214", 1607904010, 1607904050)

        self.assertEqual(result, expected)

    def test_iterate_time_range_window_at_start(self):
        abstract_input_db = AbstractInputDB(tag="log", 
                                            windows=60, 
                                            time_key="timestamp", 
                                            table_name_template="log_%Y%m%d", 
                                            table_name_match="log_*", 
                                            offset=0, 
                                            remove=False, 
                                            reload_position=False, 
                                            db_path=None)

        time_range = [
            ("log_20201214", 1607904010, 1607904050), # dec 14 0h00:10 à dec 14 00h00:50
        ]

        ranges = [x for x in abstract_input_db.iterate_time_range(time_range, 1607904000, 1607904030)] # dec 14 0h00:00 à dec 14 00h00:30
        result = ranges[0]
        expected = ("log_20201214", 1607904010, 1607904030)

        self.assertEqual(result, expected)

    def test_iterate_time_range_window_at_end(self):
        abstract_input_db = AbstractInputDB(tag="log", 
                                            windows=60, 
                                            time_key="timestamp", 
                                            table_name_template="log_%Y%m%d", 
                                            table_name_match="log_*", 
                                            offset=0, 
                                            remove=False, 
                                            reload_position=False, 
                                            db_path=None)

        time_range = [
            ("log_20201214", 1607904010, 1607904050), # dec 14 0h00:10 à dec 14 00h00:50
        ]

        ranges = [x for x in abstract_input_db.iterate_time_range(time_range, 1607904030, 1607904060)] # dec 14 0h00:30 à dec 14 00h01:00
        result = ranges[0]
        expected = ("log_20201214", 1607904030, 1607904050)

        self.assertEqual(result, expected)

    def test_iterate_time_range_well_chained(self):
        abstract_input_db = AbstractInputDB(tag="log", 
                                            windows=60, 
                                            time_key="timestamp", 
                                            table_name_template="log_%Y%m%d", 
                                            table_name_match="log_*", 
                                            offset=0, 
                                            remove=False, 
                                            reload_position=False, 
                                            db_path=None)

        time_range = [
            ("log_20201214", 1607904000, 1607904120), # dec 14 0h00 à dec 14 00h02
        ]

        result = [x for x in abstract_input_db.iterate_time_range(time_range, 1607904000, 1607904130)] # dec 14 0h00:30 à dec 14 00h01:00
        expected = [
            ("log_20201214", 1607904000, 1607904059),
            ("log_20201214", 1607904060, 1607904119)
        ]

        self.assertEqual(result, expected)


        
