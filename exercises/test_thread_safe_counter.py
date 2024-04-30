import unittest
from thread_safe_counter import Counter
import threading


class TestThreadSafeCounter(unittest.TestCase):
    def test_counter(self):
        counter = Counter()

        def worker():
            for _ in range(100000):
                counter.increment()

        threads = []
        for _ in range(5):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        self.assertEqual(counter.get_value(), 500000)


if __name__ == "__main__":
    unittest.main()
