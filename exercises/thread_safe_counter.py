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
