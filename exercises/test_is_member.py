import unittest

from is_member import is_member


class TestIsMember(unittest.TestCase):
    def test_empty_list(self):
        self.assertFalse(
            is_member("a", []), "An empty list was provided but not returned"
        )

    def test_is_member(self):
        test = ["a", "b", "c", "d", "e"]
        self.assertTrue(
            is_member("a", test), f"is_member('a', {test}) did not return correct value"
        )

    def test_is_not_member(self):
        test = ["a", "b", "c", "d", "e"]
        self.assertFalse(
            is_member("f", test), f"is_member('f', {test}) did not return correct value"
        )


if __name__ == "__main__":
    unittest.main()
