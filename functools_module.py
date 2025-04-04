"""
Functools Module Examples

This module demonstrates various utilities from the functools module including
partial, lru_cache, reduce, singledispatch, and total_ordering.
"""
import time
from functools import lru_cache, partial, reduce, singledispatch, total_ordering, wraps
from typing import Any, Callable, Dict, List, TypeVar, cast

# ----- partial: Creating specialized functions -----


def multiply(x: float, y: float) -> float:
    """Multiply two numbers."""
    return x * y


# Create specialized functions using partial
double = partial(multiply, 2)
triple = partial(multiply, 3)


# Example with keyword arguments
def format_text(text: str, prefix: str = "", suffix: str = "") -> str:
    """Format text with optional prefix and suffix."""
    return f"{prefix}{text}{suffix}"


# Create a function that wraps text in brackets
bracket_text = partial(format_text, prefix="[", suffix="]")

# ----- lru_cache: Memoization for performance -----


@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """Calculate Fibonacci numbers with caching."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_no_cache(n: int) -> int:
    """Calculate Fibonacci numbers without caching (for comparison)."""
    if n <= 1:
        return n
    return fibonacci_no_cache(n - 1) + fibonacci_no_cache(n - 2)


def demonstrate_lru_cache() -> None:
    """Show the performance benefits of lru_cache."""
    n = 35

    # Measure time with caching
    start = time.time()
    result1 = fibonacci(n)
    cached_time = time.time() - start

    # Clear the cache
    fibonacci.cache_clear()

    # Measure first-time call with empty cache
    start = time.time()
    fibonacci(n)  # Store result without unused variable
    first_time = time.time() - start

    # Measure time without caching
    start = time.time()
    fibonacci_no_cache(n - 10)  # Use smaller n to avoid excessive time
    no_cache_time = time.time() - start

    print(f"Fibonacci({n}) = {result1}")
    print(f"Time with warmed cache: {cached_time:.6f} seconds")
    print(f"Time with cold cache: {first_time:.6f} seconds")
    print(f"Time without cache (n={n-10}): {no_cache_time:.6f} seconds")


# ----- reduce: Cumulative operations -----


def sum_numbers(numbers: List[int]) -> int:
    """Sum a list of numbers using reduce."""
    return reduce(lambda a, b: a + b, numbers, 0)


def factorial(n: int) -> int:
    """Calculate factorial using reduce."""
    return reduce(lambda a, b: a * b, range(1, n + 1), 1)


def concatenate_strings(strings: List[str], separator: str = "") -> str:
    """Concatenate a list of strings using reduce."""
    if not strings:
        return ""
    return reduce(lambda a, b: f"{a}{separator}{b}", strings)


# ----- singledispatch: Function overloading based on type -----


@singledispatch
def process_data(data: Any) -> str:
    """Process data based on its type."""
    return f"Unknown type: {type(data).__name__}"


@process_data.register
def _(data: str) -> str:
    return f"Processing string: {data.upper()}"


@process_data.register
def _(data: int) -> str:
    return f"Processing integer: {data * 2}"


@process_data.register
def _(data: list) -> str:
    return f"Processing list with {len(data)} items"


@process_data.register(dict)  # Alternative registration syntax
def _(data: Dict[Any, Any]) -> str:
    return f"Processing dictionary with {len(data)} keys"


# ----- total_ordering: Complete comparison operations -----


@total_ordering
class Person:
    """Person class with comparison operations defined."""

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Person):
            return NotImplemented
        return self.age == other.age

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Person):
            return NotImplemented
        return self.age < other.age

    def __repr__(self) -> str:
        return f"Person(name='{self.name}', age={self.age})"


# ----- wraps: Preserve metadata in decorators -----

T = TypeVar("T", bound=Callable[..., Any])


def debug(func: T) -> T:
    """Decorator to print function name and arguments."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Wrapper preserving original function metadata."""
        print(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result

    return cast(T, wrapper)


@debug
def greet(name: str) -> str:
    """Function with a docstring that should be preserved."""
    return f"Hello, {name}!"


# Example usage
if __name__ == "__main__":
    # partial examples
    print("\n--- partial examples ---")
    print(f"double(5) = {double(5)}")
    print(f"triple(5) = {triple(5)}")
    print(f"bracket_text('example') = {bracket_text('example')}")

    # lru_cache examples
    print("\n--- lru_cache examples ---")
    demonstrate_lru_cache()

    # reduce examples
    print("\n--- reduce examples ---")
    print(f"sum_numbers([1, 2, 3, 4, 5]) = {sum_numbers([1, 2, 3, 4, 5])}")
    print(f"factorial(5) = {factorial(5)}")
    print(
        f"concatenate_strings(['Hello', 'World']) = {concatenate_strings(['Hello', 'World'])}"
    )
    print(
        f"concatenate_strings(['a', 'b', 'c'], '-') = {concatenate_strings(['a', 'b', 'c'], '-')}"
    )

    # singledispatch examples
    print("\n--- singledispatch examples ---")
    print(process_data("hello"))
    print(process_data(42))
    print(process_data([1, 2, 3]))
    print(process_data({"a": 1, "b": 2}))
    print(process_data(3.14))  # Uses default implementation

    # total_ordering examples
    print("\n--- total_ordering examples ---")
    alice = Person("Alice", 30)
    bob = Person("Bob", 25)
    charlie = Person("Charlie", 30)

    print(f"{alice} > {bob}: {alice > bob}")
    print(f"{alice} == {charlie}: {alice == charlie}")
    print(f"{bob} <= {charlie}: {bob <= charlie}")

    # wraps examples
    print("\n--- wraps examples ---")
    print(f"greet.__name__: {greet.__name__}")
    print(f"greet.__doc__: {greet.__doc__}")
    result = greet("Claude")
