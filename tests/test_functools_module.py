"""
Tests for the functools_module.py examples.
"""
import os
import sys

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from functools_module import (
    Person,
    bracket_text,
    concatenate_strings,
    double,
    factorial,
    fibonacci,
    fibonacci_no_cache,
    format_text,
    greet,
    multiply,
    process_data,
    sum_numbers,
    triple,
)


class TestPartial:
    """Test the partial function examples."""

    def test_multiply(self):
        """Test the base multiply function."""
        assert multiply(2, 3) == 6
        assert multiply(5, 10) == 50

    def test_double(self):
        """Test the partial function double."""
        assert double(3) == 6
        assert double(4) == 8
        assert double(0) == 0
        assert double(-5) == -10

    def test_triple(self):
        """Test the partial function triple."""
        assert triple(3) == 9
        assert triple(4) == 12
        assert triple(0) == 0
        assert triple(-5) == -15

    def test_format_text(self):
        """Test the format_text function."""
        assert format_text("hello") == "hello"
        assert format_text("hello", prefix="!") == "!hello"
        assert format_text("hello", suffix="!") == "hello!"
        assert format_text("hello", prefix="<", suffix=">") == "<hello>"

    def test_bracket_text(self):
        """Test the bracket_text partial function."""
        assert bracket_text("hello") == "[hello]"
        assert bracket_text("") == "[]"


class TestLRUCache:
    """Test the lru_cache examples."""

    def test_fibonacci(self):
        """Test the fibonacci function with cache."""
        fibonacci.cache_clear()  # Clear cache before testing
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1
        assert fibonacci(2) == 1
        assert fibonacci(5) == 5
        assert fibonacci(10) == 55

    def test_fibonacci_no_cache(self):
        """Test fibonacci without cache for correctness."""
        assert fibonacci_no_cache(0) == 0
        assert fibonacci_no_cache(1) == 1
        assert fibonacci_no_cache(5) == 5
        assert fibonacci_no_cache(10) == 55


class TestReduce:
    """Test the reduce function examples."""

    def test_sum_numbers(self):
        """Test the sum_numbers function."""
        assert sum_numbers([]) == 0
        assert sum_numbers([1, 2, 3]) == 6
        assert sum_numbers([-1, 1]) == 0
        assert sum_numbers([10]) == 10

    def test_factorial(self):
        """Test the factorial function."""
        assert factorial(0) == 1
        assert factorial(1) == 1
        assert factorial(5) == 120
        assert factorial(10) == 3628800

    def test_concatenate_strings(self):
        """Test the concatenate_strings function."""
        assert concatenate_strings([]) == ""
        assert concatenate_strings(["a"]) == "a"
        assert concatenate_strings(["a", "b", "c"]) == "abc"
        assert concatenate_strings(["a", "b", "c"], "-") == "a-b-c"
        assert concatenate_strings(["Hello", "World"], " ") == "Hello World"


class TestSingleDispatch:
    """Test the singledispatch examples."""

    def test_process_data_str(self):
        """Test processing string data."""
        assert process_data("hello") == "Processing string: HELLO"
        assert process_data("") == "Processing string: "

    def test_process_data_int(self):
        """Test processing integer data."""
        assert process_data(42) == "Processing integer: 84"
        assert process_data(0) == "Processing integer: 0"
        assert process_data(-5) == "Processing integer: -10"

    def test_process_data_list(self):
        """Test processing list data."""
        assert process_data([1, 2, 3]) == "Processing list with 3 items"
        assert process_data([]) == "Processing list with 0 items"

    def test_process_data_dict(self):
        """Test processing dictionary data."""
        assert process_data({"a": 1, "b": 2}) == ("Processing dictionary with 2 keys")
        assert process_data({}) == "Processing dictionary with 0 keys"

    def test_process_data_unknown(self):
        """Test processing data with no registered handler."""
        assert process_data(3.14).startswith("Unknown type: float")
        assert process_data(None).startswith("Unknown type: NoneType")


class TestTotalOrdering:
    """Test the total_ordering examples."""

    def test_equality(self):
        """Test equality comparisons."""
        alice = Person("Alice", 30)
        bob = Person("Bob", 25)
        charlie = Person("Charlie", 30)

        assert alice == charlie
        assert alice != bob
        assert not (alice == bob)
        assert not (bob == charlie)

    def test_less_than(self):
        """Test less than comparisons."""
        alice = Person("Alice", 30)
        bob = Person("Bob", 25)

        assert bob < alice
        assert not (alice < bob)

    def test_greater_than(self):
        """Test greater than comparisons."""
        alice = Person("Alice", 30)
        bob = Person("Bob", 25)

        assert alice > bob
        assert not (bob > alice)

    def test_less_equal(self):
        """Test less than or equal comparisons."""
        alice = Person("Alice", 30)
        bob = Person("Bob", 25)
        charlie = Person("Charlie", 30)

        assert bob <= alice
        assert alice <= charlie
        assert not (alice <= bob)

    def test_greater_equal(self):
        """Test greater than or equal comparisons."""
        alice = Person("Alice", 30)
        bob = Person("Bob", 25)
        charlie = Person("Charlie", 30)

        assert alice >= bob
        assert alice >= charlie
        assert not (bob >= alice)


class TestWraps:
    """Test the wraps decorator."""

    def test_function_metadata_preserved(self):
        """Test that function metadata is preserved."""
        assert greet.__name__ == "greet"
        assert greet.__doc__ == ("Function with a docstring that should be preserved.")

    def test_decorated_function_behavior(self, capsys):
        """Test the behavior of the decorated function."""
        result = greet("Test")
        captured = capsys.readouterr()

        assert result == "Hello, Test!"
        assert "Calling greet with args: ('Test',), kwargs: {}" in captured.out
        assert "greet returned: Hello, Test!" in captured.out
