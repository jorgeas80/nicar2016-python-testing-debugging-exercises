import os
import unittest

from results import BrokenChicagoResultsLoader, ChicagoResultsLoader

DATA_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'data')

class TestChicagoResultLoader(unittest.TestCase):
    def setUp(self):
        self._loader = ChicagoResultsLoader()
        self._data_path = os.path.join(DATA_DIRECTORY, 'summary.txt')

    def test_load(self):
        results = self._loader.load(self._data_path)
        alvarez = next(r for r in results if r['candidate_name'] == "Anita Alvarez")
        self.assertEqual(alvarez['contest_code'], '0079')
        self.assertEqual(alvarez['candidate_number'], '002')
        self.assertEqual(alvarez['votes'], 0)

    def test_parse_result_full(self):
        line = "0079002206900000000000DEM       State's Attorney, Cook County                           Anita Alvarez                         Cook County              001"
        result = self._loader.parse_result(line)
        self.assertEqual(result['candidate_name'], "Anita Alvarez")
        self.assertEqual(result['contest_code'], '0079')
        self.assertEqual(result['candidate_number'], '002')
        self.assertEqual(result['votes'], 0)
        self.assertEqual(result['party_abbreviation'], "DEM")
        self.assertEqual(result['num_eligible_precincts'], 2069)
        self.assertEqual(result['num_completed_precincts'], 0)
        self.assertEqual(result['contest_name'], "State's Attorney, Cook County")
        self.assertEqual(result['political_subdivision_name'], "Cook County")
        self.assertEqual(result['vote_for'], 1)

    def test_parse_result_numbers_only(self):    
        line = "0079002206900000000000"
        result = self._loader.parse_result(line)
        self.assertEqual(result['contest_code'], '0079')
        self.assertEqual(result['candidate_number'], '002')
        self.assertEqual(result['votes'], 0)
        self.assertEqual(result['num_eligible_precincts'], 2069)
        self.assertEqual(result['num_completed_precincts'], 0)
        self.assertNotIn('party_abbreviation', result)
        self.assertNotIn('contest_name', result)
        self.assertNotIn('political_subdivision_name', result)
        self.assertNotIn('vote_for', result)



class TestBrokenChicagoResultLoader(unittest.TestCase):
    def test_load(self):
        loader = BrokenChicagoResultsLoader()
        data_path = os.path.join(DATA_DIRECTORY, 'summary.txt')
        results = loader.load(data_path)

        alvarez = next(r for r in results if r['candidate_name'] == "Anita Alvarez")

        import pdb; pdb.set_trace()
        # In Python 3, the error is after this line. So, I add a breakpoint.
        # I'd print the variables to see what's happening

        # (pdb) from pprint import pprint
        # (pdb) pprint(alvarez)
        # {'candidate_name': 'Anita Alvarez',
        # 'candidate_number': '002',
        # 'contest_code': '0790', --> Why is this field 0790 instead of 0079? It has an offset of 1 char
        # 'contest_name': "State's Attorney, Cook County",
        # 'num_completed_precincts': 0,
        # 'num_eligible_precincts': 2069,
        # 'party_abbreviation': 'DEM',
        # 'political_subdivision_abbreviation': '',
        # 'political_subdivision_name': 'Cook County',
        # 'vote_for': 1,
        # 'votes': 0}
        #
        # Looking at contest_code, looks like it's shifted. By checking loader.load function, I see:
        # ('contest_code', 1, 4, str)
        # but it should be
        # ('contest_code', 0, 4, str),

        self.assertEqual(alvarez['contest_code'], '0079')
        self.assertEqual(alvarez['candidate_number'], '002')
        self.assertEqual(alvarez['votes'], 0)
