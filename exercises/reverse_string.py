# Prelude

# Imports
from typing import List

# Code


def reverse_string(s: str) -> str:
    """
    Reverses a string.
    """
    stack = [char for char in s]

    s = ""
    while stack:
        s += stack.pop()

    return s
