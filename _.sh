#!/bin/sh

# Create the exercises directory
mkdir -p exercises

# Exercise 1: Design Patterns
cat > exercises/design_patterns.py <<'EOL'
# Exercise: Design Patterns
# Implement a singleton pattern and a factory pattern in Python.

# Singleton Pattern
class Singleton:
    # Your code here
    pass

# Factory Pattern
class ShapeFactory:
    # Your code here
    pass

if __name__ == "__main__":
    # Test Singleton
    s1 = Singleton()
    s2 = Singleton()
    print(s1 == s2)  # Output: True

    # Test Factory
    factory = ShapeFactory()
    circle = factory.create_shape("circle")
    square = factory.create_shape("square")
    print(circle.draw())  # Output: Drawing a circle
    print(square.draw())  # Output: Drawing a square
EOL

cat > exercises/test_design_patterns.py <<'EOL'
import unittest
from design_patterns import Singleton, ShapeFactory

class TestDesignPatterns(unittest.TestCase):
    def test_singleton(self):
        s1 = Singleton()
        s2 = Singleton()
        self.assertEqual(s1, s2)

    def test_factory(self):
        factory = ShapeFactory()
        circle = factory.create_shape("circle")
        square = factory.create_shape("square")
        self.assertEqual(circle.draw(), "Drawing a circle")
        self.assertEqual(square.draw(), "Drawing a square")

if __name__ == "__main__":
    unittest.main()
EOL

# Exercise 2: Data Structures
cat > exercises/lru_cache.py <<'EOL'
# Exercise: LRU Cache
# Implement an LRU (Least Recently Used) cache in Python.

class LRUCache:
    def __init__(self, capacity):
        # Your code here
        pass

    def get(self, key):
        # Your code here
        pass

    def put(self, key, value):
        # Your code here
        pass

if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.get(1))  # Output: 1
    cache.put(3, 3)
    print(cache.get(2))  # Output: -1
EOL

cat > exercises/test_lru_cache.py <<'EOL'
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
EOL

# Exercise 3: Concurrency
cat > exercises/thread_safe_counter.py <<'EOL'
# Exercise: Thread-Safe Counter
# Implement a thread-safe counter in Python.

import threading

class Counter:
    def __init__(self):
        # Your code here
        pass

    def increment(self):
        # Your code here
        pass

    def get_value(self):
        # Your code here
        pass

if __name__ == "__main__":
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

    print(counter.get_value())  # Output: 500000
EOL

cat > exercises/test_thread_safe_counter.py <<'EOL'
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
EOL

# More exercises...

echo "Exercises and test files created successfully!"
