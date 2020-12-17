from feedoo.abstract_input_db import AbstractInputDB
import unittest
from pprint import pprint

class TestAbstractInputDB(unittest.TestCase):
    def test_1(self):
        abstract_input_db = AbstractInputDB(tag="log", 
                                            windows=60, 
                                            time_key="timestamp", 
                                            table_name_match="log_*", 
                                            offset=0, 
                                            remove=False, 
                                            reload_position=False, 
                                            db_path=None)

    def test_get_matching_table(self):
        abstract_input_db = AbstractInputDB(tag="log", 
                                            windows=60, 
                                            time_key="timestamp", 
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
        expected = ("log_20201214", 1607904010, 1607904029)

        self.assertEqual(result, expected)

    def test_iterate_time_range_window_at_end(self):
        abstract_input_db = AbstractInputDB(tag="log", 
                                            windows=60, 
                                            time_key="timestamp", 
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
            ("log_20201214", 1607904060, 1607904119),
            ('log_20201214', 1607904120, 1607904120)
        ]

        self.assertEqual(result, expected)

    def test_iterate_time_last_table_element(self):
        abstract_input_db = AbstractInputDB(tag="log", 
                                            windows=3600, 
                                            time_key="timestamp", 
                                            table_name_match="log_*", 
                                            offset=0, 
                                            remove=False, 
                                            reload_position=False, 
                                            db_path=None)

        time_range = [
            ("log_20201214", 1607904000, 1607990399), # dec 14 0h00 à dec 14 23h59:59
            ("log_20201215", 1607990400, 1608076799) # dec 15 0h00 à dec 15 23h59:59
        ]

        result = [x for x in abstract_input_db.iterate_time_range(time_range, 0, 1608055200)] # 0 to dec 15 18h00
        expected = [('log_20201214', 1607904000, 1607907599),
            ('log_20201214', 1607907600, 1607911199),
            ('log_20201214', 1607911200, 1607914799),
            ('log_20201214', 1607914800, 1607918399),
            ('log_20201214', 1607918400, 1607921999),
            ('log_20201214', 1607922000, 1607925599),
            ('log_20201214', 1607925600, 1607929199),
            ('log_20201214', 1607929200, 1607932799),
            ('log_20201214', 1607932800, 1607936399),
            ('log_20201214', 1607936400, 1607939999),
            ('log_20201214', 1607940000, 1607943599),
            ('log_20201214', 1607943600, 1607947199),
            ('log_20201214', 1607947200, 1607950799),
            ('log_20201214', 1607950800, 1607954399),
            ('log_20201214', 1607954400, 1607957999),
            ('log_20201214', 1607958000, 1607961599),
            ('log_20201214', 1607961600, 1607965199),
            ('log_20201214', 1607965200, 1607968799),
            ('log_20201214', 1607968800, 1607972399),
            ('log_20201214', 1607972400, 1607975999),
            ('log_20201214', 1607976000, 1607979599),
            ('log_20201214', 1607979600, 1607983199),
            ('log_20201214', 1607983200, 1607986799),
            ('log_20201214', 1607986800, 1607990399),
            ('log_20201215', 1607990400, 1607993999),
            ('log_20201215', 1607994000, 1607997599),
            ('log_20201215', 1607997600, 1608001199),
            ('log_20201215', 1608001200, 1608004799),
            ('log_20201215', 1608004800, 1608008399),
            ('log_20201215', 1608008400, 1608011999),
            ('log_20201215', 1608012000, 1608015599),
            ('log_20201215', 1608015600, 1608019199),
            ('log_20201215', 1608019200, 1608022799),
            ('log_20201215', 1608022800, 1608026399),
            ('log_20201215', 1608026400, 1608029999),
            ('log_20201215', 1608030000, 1608033599),
            ('log_20201215', 1608033600, 1608037199),
            ('log_20201215', 1608037200, 1608040799),
            ('log_20201215', 1608040800, 1608044399),
            ('log_20201215', 1608044400, 1608047999),
            ('log_20201215', 1608048000, 1608051599),
            ('log_20201215', 1608051600, 1608055199)]
        self.assertEqual(result, expected)



        
