import unittest

def pruebame(items):
    if not items:
        return []
    if len(items) == 1:
        return [items[0].upper()]
    if any(type(x) is not str for x in items):
        return []
        
    return [items[1].upper(), items[0].upper()]

class PruebameTestCase(unittest.TestCase):
    def test_empty_items(self):
        res = pruebame([])
        self.assertListEqual(res, [])

    def test_just_one_item(self):
        test_list = ["foo"]
        res = pruebame(test_list)
        self.assertListEqual(res, ["FOO"])

    def test_more_than_two_items(self):
        test_list = ["foo", "bar", "baz"]
        res = pruebame(test_list)
        self.assertListEqual(res, ["BAR", "FOO"])

    def test_list_of_not_strings(self):
        test_list = [1, 2]
        res = pruebame(test_list)
        self.assertListEqual(res, [])
