import unittest

from reverse_string import reverse_string


class TestReverseString(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(
            reverse_string(""), "", "An empty string was provided but not returned"
        )

    def test_reverse_string(self):
        self.assertEqual(
            reverse_string("hello"),
            "olleh",
            "reverse_string('hello') did not return correct value",
        )


if __name__ == "__main__":
    unittest.main()
