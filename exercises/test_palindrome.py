import unittest
from palindrome import is_palindrome


class TestPalindrome(unittest.TestCase):
    def test_is_palindrome(self):
        self.assertTrue(is_palindrome("racecar"))
        self.assertFalse(is_palindrome("hello"))


if __name__ == "__main__":
    unittest.main()
