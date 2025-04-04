import unittest

from topk import top_k


class TestTopK(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(
            top_k([], 1), [], "An empty list was provided but not returned"
        )

    def test_top_2(self):
        test = ["a", "b", "c", "d", "e", "a", "b"]
        self.assertEqual(
            top_k(test, 2), ["a", "b"], f"top_k({test}, 2) did not return correct value"
        )

    def test_top_3(self):
        test = ["a", "b", "c", "d", "e", "a", "b", "e", "e"]
        self.assertEqual(
            top_k(test, 3),
            ["e", "a", "b"],
            f"top_k({test}, 3) did not return correct value",
        )


if __name__ == "__main__":
    unittest.main()
