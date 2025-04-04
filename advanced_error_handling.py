#!/usr/bin/env python3
"""
Advanced Error Handling in Python
================================

This module demonstrates advanced error handling techniques in Python
beyond basic try/except blocks, including:

- Custom exception hierarchies
- Context-specific exceptions
- Exception chaining
- Context managers for cleanup
- Handling asynchronous exceptions
- Error reporting and logging strategies

Designed to work well with IPython for interactive exploration.
"""

import contextlib
import logging
import sys
import traceback
from typing import Any, Callable, Optional, TypeVar, Union

# Configure basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Custom Exception Hierarchy
class ApplicationError(Exception):
    """Base exception class for all application errors."""

    def __init__(self, message: str, *args, **kwargs):
        self.message = message
        super().__init__(message, *args, **kwargs)


class ConfigurationError(ApplicationError):
    """Error raised when there's an issue with application configuration."""

    pass


class ValidationError(ApplicationError):
    """Error raised when validation fails."""

    def __init__(self, message: str, field: str = None, *args, **kwargs):
        self.field = field
        error_msg = f"{message}" if field is None else f"{field}: {message}"
        super().__init__(error_msg, *args, **kwargs)


class DatabaseError(ApplicationError):
    """Base class for database-related errors."""

    pass


class ConnectionError(DatabaseError):
    """Error raised when database connection fails."""

    def __init__(self, message: str, host: str = None, *args, **kwargs):
        self.host = host
        error_msg = message
        if host:
            error_msg = f"Failed to connect to {host}: {message}"
        super().__init__(error_msg, *args, **kwargs)


class QueryError(DatabaseError):
    """Error raised when a database query fails."""

    def __init__(self, message: str, query: str = None, *args, **kwargs):
        self.query = query
        error_msg = message
        if query:
            # Truncate long queries for readability
            query_display = query if len(query) < 50 else f"{query[:47]}..."
            error_msg = f"Query failed: {message} - SQL: {query_display}"
        super().__init__(error_msg, *args, **kwargs)


# Exception Chaining Example
def fetch_data(query: str) -> list:
    """Simulates fetching data with exception chaining."""
    try:
        # Simulate a database error
        if "invalid" in query.lower():
            raise ValueError("Invalid SQL syntax")

        # Return mock data
        return [{"id": 1, "name": "Test"}]

    except ValueError as e:
        # Preserve the original exception and add context
        raise QueryError("Could not execute query", query=query) from e


# Context Managers for Resource Management
@contextlib.contextmanager
def database_connection(host: str, database: str) -> Any:
    """Context manager for database connections with proper error handling."""
    connection = None
    try:
        # Simulate connecting to a database
        logger.info(f"Connecting to {database} on {host}...")

        # Simulate connection failure
        if host == "invalid":
            raise ConnectionError("Connection refused", host=host)

        connection = {"host": host, "database": database, "connected": True}
        logger.info("Connected successfully")

        # Yield the connection to the caller
        yield connection

    except Exception as e:
        # Log the exception but allow it to propagate
        logger.error(f"Database error: {e}")
        raise

    finally:
        # Ensure connection cleanup happens regardless of exceptions
        if connection and connection.get("connected"):
            logger.info("Closing connection...")
            connection["connected"] = False


# Retry Decorator with Exponential Backoff
def retry(
    exceptions: Union[Exception, tuple],
    tries: int = 4,
    delay: float = 1.0,
    backoff: float = 2.0,
    logger: Optional[logging.Logger] = None,
) -> Callable:
    """
    Retry decorator with exponential backoff for handling transient errors.

    Args:
        exceptions: The exception(s) to catch and retry on
        tries: Number of times to try before giving up
        delay: Initial delay between retries in seconds
        backoff: Backoff multiplier
        logger: Logger to use for logging retries

    Returns:
        A decorator function
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            mtries, mdelay = tries, delay
            last_exception = None

            while mtries > 0:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    mtries -= 1
                    if mtries == 0:
                        break

                    if logger:
                        logger.warning(
                            f"Retrying {func.__name__} in {mdelay:.2f}s due to {e}"
                        )

                    # Sleep with backoff
                    import time

                    time.sleep(mdelay)
                    mdelay *= backoff

            # Reraise the last exception when out of retries
            if last_exception:
                raise last_exception

        return wrapper

    return decorator


# Example of using the retry decorator
@retry(exceptions=(ConnectionError, QueryError), logger=logger)
def unstable_operation() -> str:
    """A simulated unstable operation that might fail transiently."""
    import random

    # Simulate random failures
    failure_chance = random.random()
    if failure_chance < 0.7:  # 70% chance of failure
        if failure_chance < 0.3:
            raise ConnectionError("Temporary network issue", host="db.example.com")
        else:
            raise QueryError("Query timeout", query="SELECT * FROM large_table")

    return "Operation succeeded"


# Error Boundary Context Manager
@contextlib.contextmanager
def error_boundary(
    error_handler: Callable[[Exception], Any] = None,
    catch_exceptions: tuple = (Exception,),
    reraise: bool = False,
) -> None:
    """
    Context manager that implements an error boundary pattern.

    Args:
        error_handler: Function to call with the exception
        catch_exceptions: Types of exceptions to catch
        reraise: Whether to reraise the exception after handling
    """
    try:
        yield
    except catch_exceptions as e:
        if error_handler:
            error_handler(e)

        if reraise:
            raise


# Enhanced Exception Handling with Detailed Reporting
def handle_exception(e: Exception) -> None:
    """
    Handle an exception with detailed reporting.

    Args:
        e: The exception to handle
    """
    # Get exception details
    exc_type, exc_value, exc_traceback = sys.exc_info()

    # Format exception for logging
    trace_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    traceback_text = "".join(trace_lines)

    # Extract the last frame for context
    try:
        last_frame = traceback.extract_tb(exc_traceback)[-1]
        filename, line, func, code = last_frame
        context = f"in {func} at {filename}:{line}\n  {code}"
    except (IndexError, AttributeError):
        context = "Context not available"

    # Log the detailed exception
    logger.error(f"Exception: {exc_type.__name__}: {exc_value}")
    logger.error(f"Context: {context}")
    logger.debug(f"Traceback:\n{traceback_text}")

    # Check for exception chaining
    if e.__cause__:
        logger.error(f"Caused by: {type(e.__cause__).__name__}: {e.__cause__}")


# Practical Examples
def examples():
    """Run practical examples of advanced error handling."""
    print("\n1. Try-except with specific exception types:")
    try:
        user_id = "abc"  # Should be an integer
        user_id = int(user_id)
        print(f"User ID: {user_id}")
    except ValueError as e:
        print(f"Invalid user ID format: {e}")

    print("\n2. Using the custom exception hierarchy:")
    try:
        if len("test_password") < 10:
            raise ValidationError("Password too short", field="password")
    except ValidationError as e:
        print(f"Validation failed: {e}")

    print("\n3. Using a context manager for resource management:")
    try:
        with database_connection("localhost", "test_db") as conn:
            print(f"Using connection to {conn['database']}")
            # This would fail:
            # raise QueryError("Query timeout")
    except DatabaseError as e:
        print(f"Database operation failed: {e}")

    print("\n4. Exception chaining example:")
    try:
        result = fetch_data("SELECT * FROM invalid_table")
        print(f"Data: {result}")
    except QueryError as e:
        print(f"Query error: {e}")
        if e.__cause__:
            print(f"Original error: {e.__cause__}")

    print("\n5. Retry mechanism for unstable operations:")
    try:
        result = unstable_operation()
        print(f"Result: {result}")
    except (ConnectionError, QueryError) as e:
        print(f"Operation failed after multiple retries: {e}")

    print("\n6. Error boundary pattern:")
    with error_boundary(
        error_handler=lambda e: print(f"Caught error: {type(e).__name__}: {e}"),
        catch_exceptions=(ValueError, TypeError),
    ):
        # This will be caught by the error boundary
        x = "5" + 5


# Interactive Exercises
def exercises():
    """Exercises for advanced error handling"""
    print("\nExercises:")

    # Exercise 1: Implement custom exceptions for a banking system
    print("Exercise 1: Implement custom exceptions for a banking system")
    # Your solution here

    # Exercise 2: Create a context manager for file operations with error handling
    print("Exercise 2: Create a context manager for file operations")
    # Your solution here

    # Exercise 3: Implement a robust HTTP client with retry logic
    print("Exercise 3: Implement a robust HTTP client with retry logic")
    # Your solution here


# Main function
if __name__ == "__main__":
    print("Advanced Error Handling in Python\n")

    # Run practical examples
    examples()

    # Run exercises
    exercises()
