import unittest

from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def test_lru_cache(self):
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        self.assertEqual(cache.get(1), 1)
        cache.put(3, 3)
        self.assertEqual(cache.get(2), -1)


if __name__ == "__main__":
    unittest.main()
