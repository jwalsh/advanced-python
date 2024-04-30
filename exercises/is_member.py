# Prelude 
# Check if a string is a valid member of a list of strings.

# Problem
# Given a list of strings, write a function to check if a given string is a valid member of the list.

# Imports 
from typing import List

def is_member(lst: List[str], s: str) -> bool:
    """
    Check if a string is a valid member of a list of strings.
    """
    return s in lst

def is_member_loop(lst: List[str], s: str) -> bool:
    """
    Check if a string is a valid member of a list of strings.
    """
    for item in lst:
        if item == s:
            return True
    return False
