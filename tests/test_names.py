# -*- coding: utf-8 -*
import unittest

from names import parse_names

class TestNames(unittest.TestCase):
    def test_parse_names(self):
        test_values = [
            ("Hing,Geoff,George", {
                "first_name": "Geoff",
                "last_name": "Hing",
                "middle_name": "George",
                "suffix": None,
            }),
            ("Hing, Geoff, George", {
                "first_name": "Geoff",
                "last_name": "Hing",
                "middle_name": "George",
                "suffix": None,
            }),
            ("Hing, Geoff", {
                "first_name": "Geoff",
                "last_name": "Hing",
                "middle_name": None,
                "suffix": None,
            }),
            # Ida B. Wells named her daughter Ida Jr. 😻
            # http://photoarchive.lib.uchicago.edu/db.xqy?one=apf1-08624.xml
            ("Wells, Ida, B., Jr.", {
                "first_name": "Ida",
                "last_name": "Wells",
                "middle_name": "B.",
                "suffix": "Jr.",
            })
        ]
        for input_string, expected in test_values:
            self.assertEqual(parse_names(input_string), expected)
