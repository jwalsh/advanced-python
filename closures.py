#!/usr/bin/env python3
"""
Closures in Python
================

This module demonstrates Python closures - functions that remember values
from their enclosing lexical scope even when executed outside that scope.

Closures are a powerful way to create functions with "memory" and are
fundamental to understanding decorators, function factories, and callbacks.

Designed to work well with IPython for interactive exploration.
"""

# Basic Closure Example
def make_counter():
    """Create a counter function using a closure"""
    count = 0
    
    def counter():
        nonlocal count
        count += 1
        return count
    
    return counter

# Function Factory Example
def make_multiplier(factor):
    """Create a function that multiplies by a specific factor"""
    def multiplier(x):
        return x * factor
    
    return multiplier

# Closure for Memoization
def memoize(func):
    """Create a memoizing version of a function using closures"""
    cache = {}
    
    def memoized_func(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    
    return memoized_func

# Example of closure with changing value (requires nonlocal)
def make_accumulator(initial_value=0):
    """Create an accumulator function"""
    total = initial_value
    
    def accumulator(value):
        nonlocal total
        total += value
        return total
    
    return accumulator

# Advanced example: Configurable logger
def create_logger(logger_name, min_level=0):
    """Create a logger function with configurable minimum level"""
    levels = {
        0: "DEBUG",
        1: "INFO",
        2: "WARNING",
        3: "ERROR",
        4: "CRITICAL"
    }
    
    def log(level, message):
        if level >= min_level:
            print(f"[{logger_name}] {levels.get(level, 'UNKNOWN')}: {message}")
    
    return log

# Example: Event handler with state
def create_event_handler():
    """Create an event handler with persistent state"""
    events = []
    
    def handler(event=None):
        if event:
            events.append(event)
            return f"Event '{event}' registered"
        else:
            return events
    
    return handler

# Exercise: Create a function factory for generating HTML tag functions
def make_tag_function(tag_name):
    """Create a function that wraps content in an HTML tag"""
    def tag_function(content):
        return f"<{tag_name}>{content}</{tag_name}>"
    
    return tag_function

# Interactive Exercises
def exercises():
    """Exercises for closures"""
    # Exercise 1: Create a password validator closure
    # It should return a function that checks if a password meets a minimum length
    print("Exercise 1:")
    # Your solution here
    
    # Exercise 2: Create a sequence generator that yields fibonacci numbers
    print("Exercise 2:")
    # Your solution here
    
    # Exercise 3: Create a throttle function that limits how often a function can be called
    print("Exercise 3:")
    # Your solution here

# Main function
if __name__ == "__main__":
    print("Closures in Python\n")
    
    # Basic counter example
    print("Counter example:")
    counter = make_counter()
    print(counter())  # 1
    print(counter())  # 2
    print(counter())  # 3
    print()
    
    # Function factory example
    print("Multiplier example:")
    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(f"double(5) = {double(5)}")  # 10
    print(f"triple(5) = {triple(5)}")  # 15
    print()
    
    # Memoization example
    print("Memoization example:")
    @memoize
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    print(f"fibonacci(30) = {fibonacci(30)}")  # Fast due to memoization
    print()
    
    # Accumulator example
    print("Accumulator example:")
    acc = make_accumulator(10)
    print(acc(5))  # 15
    print(acc(3))  # 18
    print(acc(2))  # 20
    print()
    
    # Logger example
    print("Logger example:")
    debug_logger = create_logger("DEBUG_LOGGER", 0)
    error_logger = create_logger("ERROR_LOGGER", 3)
    
    debug_logger(0, "This is a debug message")
    debug_logger(2, "This is a warning message")
    error_logger(2, "This warning won't be logged")
    error_logger(3, "This error will be logged")
    print()
    
    # Event handler example
    print("Event handler example:")
    handler = create_event_handler()
    print(handler("Button clicked"))
    print(handler("Form submitted"))
    print(f"Events: {handler()}")
    print()
    
    # HTML tag function example
    print("HTML tag function example:")
    h1 = make_tag_function("h1")
    p = make_tag_function("p")
    print(h1("Welcome to Closures"))
    print(p("This is a paragraph about closures."))
    print()
    
    # Run exercises
    print("Exercises:")
    exercises()