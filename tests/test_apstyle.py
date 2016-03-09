import unittest

from apstyle.numbers import format_cardinal_number

class ApStyleNumbersTestCase(unittest.TestCase):
    def test_format_cardinal_number(self):
        self.assertEqual(format_cardinal_number(1), "one")
        self.assertEqual(format_cardinal_number(10), "10")
        self.assertEqual(format_cardinal_number(1050), "1,050")
        self.assertEqual(format_cardinal_number(2000000), "2 million")
