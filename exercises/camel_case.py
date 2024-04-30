# Prelude

# Imports
import typing


# Code
def to_camel_case(str: str) -> str:
    """
    Converts a snake_case string to a camelCase string for underscore or hyphen separated words.
    """
    components = str.replace("_", "-").split("-")
    return components[0] + "".join(x.title() for x in components[1:])
