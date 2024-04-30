# Exercise: Rate Limiter
# Implement a rate limiter to control the rate of requests to an API.

import time


class RateLimiter:
    def __init__(self, limit, window):
        # Your code here
        pass

    def allow_request(self):
        # Your code here
        pass


if __name__ == "__main__":
    rate_limiter = RateLimiter(5, 10)  # 5 requests per 10 seconds

    for _ in range(10):
        if rate_limiter.allow_request():
            print("Request allowed")
        else:
            print("Request blocked")
        time.sleep(1)
