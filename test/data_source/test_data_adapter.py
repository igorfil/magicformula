import unittest

from data_source.data_adapter import pick_keys

class DataAdapterTest(unittest.TestCase):
    def test_can_pick_from_empty(self):
        self.assertEqual({"a": ''}, pick_keys({}, {"a": "a"}))
        self.assertEqual({"a": ''}, pick_keys(None, {"a": "a"}))

    def test_can_pick_some_keys(self):
        self.assertEqual({"a": 1}, pick_keys({"a": 1}, {"a": "a"}))
        self.assertEqual({"a": 1}, pick_keys({"a": 1, "b": 2}, {"a": "a"}))
        self.assertEqual({"a": 1, "b": 2}, pick_keys({"a": 1, "b": 2, "c": 3}, {"a": "a", "b": "b"}))

    def test_can_pick_and_map_keys(self):
        self.assertEqual({"A": 1}, pick_keys({"a": 1}, {"a": "A"}))
        self.assertEqual({"A": 1, "B": 2}, pick_keys({"a": 1, "b": 2}, {"a": "A", "b": "B"}))
