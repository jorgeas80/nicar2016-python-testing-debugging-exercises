import os
import unittest

from results import BrokenChicagoResultsLoader, ChicagoResultsLoader

DATA_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'data')

class TestChicagoResultLoader(unittest.TestCase):
    def test_load(self):
        loader = ChicagoResultsLoader()
        data_path = os.path.join(DATA_DIRECTORY, 'summary.txt')
        results = loader.load(data_path)
        alvarez = next(r for r in results if r['candidate_name'] == "Anita Alvarez")
        self.assertEqual(alvarez['contest_code'], '0079')
        self.assertEqual(alvarez['candidate_number'], '002')
        self.assertEqual(alvarez['votes'], 0)


class TestBrokenChicagoResultLoader(unittest.TestCase):
    def test_load(self):
        loader = BrokenChicagoResultsLoader()
        data_path = os.path.join(DATA_DIRECTORY, 'summary.txt')
        results = loader.load(data_path)

        alvarez = next(r for r in results if r['candidate_name'] == "Anita Alvarez")
        self.assertEqual(alvarez['contest_code'], '0079')
        self.assertEqual(alvarez['candidate_number'], '002')
        self.assertEqual(alvarez['votes'], 0)
