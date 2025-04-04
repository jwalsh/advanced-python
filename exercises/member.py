from typing import Any, List, Optional

import click


def car(lst: List[Any]) -> Any:
    return lst[0]


def cdr(lst: List[Any]) -> Optional[List[Any]]:
    if len(lst) == 1:
        return None
    else:
        return lst[1:]


def member_p_recursion(x: Any, lst: List[Any]) -> bool:
    """
    Checks if a given element is a member of a list using recursion.
    :param x: The element to search for in the list.
    :param lst: The list to search for the element.
    :return: True if the element is found in the list, False otherwise.
    """
    if lst is None:
        return False
    elif x == car(lst):
        return True
    else:
        return member_p_recursion(x, cdr(lst))


def member_p_loop(x: Any, lst: List[Any]) -> bool:
    """
    Checks if a given element is a member of a list using a loop.
    :param x: The element to search for in the list.
    :param lst: The list to search for the element.
    :return: True if the element is found in the list, False otherwise.
    """
    if lst is None:
        return False
    else:
        for element in lst:
            if x == element:
                return True
        return False


def member_p_fold(x: Any, lst: List[Any]) -> bool:
    """
    Checks if a given element is a member of a list using the fold (reduce) function.
    :param x: The element to search for in the list.
    :param lst: The list to search for the element.
    :return: True if the element is found in the list, False otherwise.
    """
    from functools import reduce

    return reduce(lambda acc, y: acc or y == x, lst, False)


member_p_tests = [
    {
        "name": "Three is a member of the list",
        "input_x": 3,
        "input_lst": [1, 2, 3, 4, 5],
        "expected": True,
    },
    {
        "name": "Three is not a member of the list",
        "input_x": 3,
        "input_lst": [1, 2, 4, 5],
        "expected": False,
    },
    {
        "name": "Three is not a member of an empty list",
        "input_x": 3,
        "input_lst": [],
        "expected": False,
    },
    {
        "name": "Three is a member of a list with only three",
        "input_x": 3,
        "input_lst": [3],
        "expected": True,
    },
    {
        "name": "Three is not a member of a list with only four",
        "input_x": 3,
        "input_lst": [4],
        "expected": False,
    },
    {
        "name": "Three is not a member of a null list",
        "input_x": 3,
        "input_lst": None,
        "expected": False,
    },
]


def run_tests(member_p_func):
    for test in member_p_tests:
        expected = test["expected"]
        result = member_p_func(test["input_x"], test["input_lst"])
        assert expected == result, test["name"]
    click.echo(f"All tests passed for {member_p_func.__name__}")


@click.command()
@click.option(
    "--method",
    type=click.Choice(["recursion", "loop", "fold"]),
    default="recursion",
    help="Method to check membership (recursion, loop, or fold)",
)
def main(method):
    if method == "recursion":
        run_tests(member_p_recursion)
    elif method == "loop":
        run_tests(member_p_loop)
    elif method == "fold":
        run_tests(member_p_fold)


if __name__ == "__main__":
    main()
