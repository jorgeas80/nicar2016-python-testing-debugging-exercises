import unittest

class NoFailuresTestCase(unittest.TestCase):
    def test_true_is_true(self):
        self.assertEqual(True, True)

    def test_false_is_fase(self):
        self.assertEqual(False, False)


class FailingTestCase(unittest.TestCase):
    def test_true_is_true(self):
        self.assertEqual(True, True)
