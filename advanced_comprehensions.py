#!/usr/bin/env python3
"""
Advanced Comprehensions in Python
================================

This module demonstrates advanced uses of comprehensions in Python,
including list, dict, set, and generator comprehensions with
nested loops, conditionals, and transformations.

Designed to work well with IPython for interactive exploration.
"""

# Basic Comprehension Examples
def basic_comprehensions():
    """Demonstrate basic comprehension syntax"""
    # List comprehension
    squares = [x**2 for x in range(10)]
    print(f"Squares: {squares}")
    
    # Dict comprehension
    square_map = {x: x**2 for x in range(10)}
    print(f"Square map: {square_map}")
    
    # Set comprehension
    even_squares = {x**2 for x in range(10) if x % 2 == 0}
    print(f"Even squares: {even_squares}")
    
    # Generator comprehension (note the parentheses)
    gen = (x**2 for x in range(10))
    print(f"Generator: {gen}")
    print(f"Generator values: {list(gen)}")

# Nested Comprehensions
def nested_comprehensions():
    """Demonstrate nested comprehensions"""
    # Nested list comprehension - flattening a matrix
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = [x for row in matrix for x in row]
    print(f"Flattened matrix: {flattened}")
    
    # Creating a matrix with comprehension
    size = 3
    identity = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
    print(f"Identity matrix:\n{identity[0]}\n{identity[1]}\n{identity[2]}")
    
    # Nested dict comprehension
    nested_dict = {
        f"key_{i}": {f"subkey_{j}": i * j for j in range(3)}
        for i in range(3)
    }
    print(f"Nested dictionary: {nested_dict}")

# Comprehensions with Conditionals
def conditional_comprehensions():
    """Demonstrate comprehensions with complex conditionals"""
    # Multiple conditions
    numbers = list(range(20))
    filtered = [x for x in numbers if x % 2 == 0 if x % 3 == 0]
    print(f"Numbers divisible by both 2 and 3: {filtered}")
    
    # If-else in comprehension (ternary expressions)
    categorized = ["even" if x % 2 == 0 else "odd" for x in range(10)]
    print(f"Even/odd categorization: {categorized}")
    
    # Filter and transform
    transformed = [x**2 if x % 2 == 0 else x**3 for x in range(10)]
    print(f"Transformed values: {transformed}")

# Advanced Transformations
def advanced_transformations():
    """Demonstrate advanced transformations in comprehensions"""
    # Using zip in comprehension
    keys = ["a", "b", "c"]
    values = [1, 2, 3]
    dict_from_lists = {k: v for k, v in zip(keys, values)}
    print(f"Dictionary from lists: {dict_from_lists}")
    
    # Comprehension with function calls
    def process(x):
        return x * 10 if x > 5 else x
    
    processed = [process(x) for x in range(10)]
    print(f"Processed values: {processed}")
    
    # Dictionary inversion with comprehension
    original = {"a": 1, "b": 2, "c": 3}
    inverted = {v: k for k, v in original.items()}
    print(f"Inverted dictionary: {inverted}")

# Example: Word frequency counter
def word_frequency_example(text):
    """Count word frequencies using comprehensions"""
    # Lowercase and split the text
    words = text.lower().split()
    
    # Remove punctuation from words
    words = [word.strip(".,!?;:()[]{}\"'") for word in words]
    
    # Count frequencies using a dict comprehension
    frequencies = {word: words.count(word) for word in set(words)}
    
    # Sort by frequency (descending)
    sorted_words = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    
    return dict(sorted_words)

# Interactive Exercises
def exercises():
    """Exercises for advanced comprehensions"""
    # Exercise 1: Create a list of tuples containing (number, square, cube)
    # for numbers 1-10
    print("Exercise 1:")
    # Your solution here
    
    # Exercise 2: Given a list of strings, create a dictionary mapping 
    # each string to its length, but only for strings with length > 3
    strings = ["a", "ab", "abc", "abcd", "abcde", "abcdef"]
    print("Exercise 2:")
    # Your solution here
    
    # Exercise 3: Create a nested dictionary where keys are the first letters 
    # of words and values are dictionaries mapping words to their lengths
    words = ["apple", "banana", "apricot", "cherry", "blueberry", "cantaloupe"]
    print("Exercise 3:")
    # Your solution here

# Main function
if __name__ == "__main__":
    print("Advanced Comprehensions in Python\n")
    
    print("Basic Comprehensions:")
    basic_comprehensions()
    print()
    
    print("Nested Comprehensions:")
    nested_comprehensions()
    print()
    
    print("Conditional Comprehensions:")
    conditional_comprehensions()
    print()
    
    print("Advanced Transformations:")
    advanced_transformations()
    print()
    
    sample_text = """
    Python is a programming language that lets you work quickly and
    integrate systems more effectively. Python is powerful and fast,
    plays well with others, runs everywhere, is friendly and easy to learn.
    Python is developed under an OSI-approved open source license, making it
    freely usable and distributable, even for commercial use.
    """
    
    print("Word Frequency Example:")
    frequencies = word_frequency_example(sample_text)
    for word, count in list(frequencies.items())[:10]:  # Top 10 words
        print(f"  {word}: {count}")
    print()
    
    print("Exercises:")
    exercises()