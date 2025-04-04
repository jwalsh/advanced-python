import unittest

from rate_limiter import RateLimiter


class TestRateLimiter(unittest.TestCase):
    def test_rate_limiter(self):
        rate_limiter = RateLimiter(5, 10)

        # Allow 5 requests
        for _ in range(5):
            self.assertTrue(rate_limiter.allow_request())

        # Block the next request
        self.assertFalse(rate_limiter.allow_request())


if __name__ == "__main__":
    unittest.main()
