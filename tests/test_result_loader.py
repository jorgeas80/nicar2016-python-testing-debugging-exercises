import unittest

from results import SimpleResultLoader

class SimpleResultLoaderTestCase(unittest.TestCase):
    def test_load_bad_json(self):
        sample_json = """
        {
          "results": [
        }
        """
        loader = SimpleResultLoader()
        results = loader.load(sample_json)
        self.assertEqual(results, [])


