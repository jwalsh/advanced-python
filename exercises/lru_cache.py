# Exercise: LRU Cache
# Implement an LRU (Least Recently Used) cache in Python.

from collections import OrderedDict

@dataclass
class LRUCache:
    def __init__(self, capacity):
        capacity = capacity
        cache = OrderedDict()

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
