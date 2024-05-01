# Decorators Exercise

# Imports 
import time

# Exercise 1: Create a decorator that prints the time taken by a function to execute
def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Time taken to execute {func.__name__}: {end - start}")
        return result
    return wrapper

# Exercise 2: Create a decorator that prints the arguments passed to a function
def print_args(func):
    def wrapper(*args, **kwargs):
        print(f"Arguments passed to {func.__name__}: {args}, {kwargs}")
        return func(*args, **kwargs)
    return wrapper

# TODO: Complete the exercise
@time_it
def fibonacci_bad(n):
    if n <= 1:
        return n
    return fibonacci_bad(n - 1) + fibonacci_bad(n - 2)

@print_args
def fizzbuzz(n):
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)

if __name__ == "__main__":
    print(fibonacci_bad(30))
    fizzbuzz(15)
