import re
from typing import Callable, Dict, List, Tuple, Union

import click

Expression = Union[int, str, Tuple[str, "Expression", "Expression"]]


def parse_and_apply_lambda(expr: str, arg: int) -> Tuple[int, List[str]]:
    """
    Parse a lambda expression and apply it to an argument.

    Args:
        expr (str): The lambda expression as a string.
        arg (int): The argument to apply to the lambda expression.

    Returns:
        Tuple[int, List[str]]: The result of applying the lambda expression and a list of evaluation steps.

    Raises:
        ValueError: If the lambda expression is invalid or contains unknown operators.
    """
    # Extract the parameter and body of the lambda expression
    match = re.match(r"λ(\w+)\.(.*)", expr)
    if not match:
        raise ValueError("Invalid lambda expression")

    param, body = match.groups()

    def parse_expr(expr: str) -> Expression:
        """
        Parse a single expression within the lambda body.

        Args:
            expr (str): The expression to parse.

        Returns:
            Expression: The parsed expression as a nested structure.

        Raises:
            ValueError: If unable to parse the expression.
        """
        expr = expr.strip()
        if expr.isdigit():
            return int(expr)
        elif expr.isalpha():
            return expr
        elif expr.startswith("(") and expr.endswith(")"):
            # Remove outer parentheses
            expr = expr[1:-1].strip()

            # Find the main operator
            paren_count = 0
            for i, char in enumerate(expr):
                if char == "(":
                    paren_count += 1
                elif char == ")":
                    paren_count -= 1
                elif char in "+-*" and paren_count == 0:
                    op = char
                    left = expr[:i].strip()
                    right = expr[i + 1 :].strip()
                    return (op, parse_expr(left), parse_expr(right))

            # If no operator found at top level, parse the expression without outer parentheses
            return parse_expr(expr)
        else:
            raise ValueError(f"Unable to parse expression: {expr}")

    parsed_body = parse_expr(body)

    def evaluate_step_by_step(
        expr: Expression, env: Dict[str, int]
    ) -> Tuple[int, List[str]]:
        """
        Evaluate the parsed expression step by step.

        Args:
            expr (Expression): The parsed expression to evaluate.
            env (Dict[str, int]): The environment containing variable bindings.

        Returns:
            Tuple[int, List[str]]: The result of the evaluation and a list of evaluation steps.

        Raises:
            ValueError: If an unknown operator is encountered.
        """
        steps = []

        def evaluate(expr: Expression, env: Dict[str, int]) -> int:
            if isinstance(expr, int):
                return expr
            elif isinstance(expr, str):
                return env.get(expr, expr)
            else:
                op, left, right = expr
                left_val = evaluate(left, env)
                right_val = evaluate(right, env)
                result = None
                if op == "+":
                    result = left_val + right_val
                elif op == "-":
                    result = left_val - right_val
                elif op == "*":
                    result = left_val * right_val
                else:
                    raise ValueError(f"Unknown operator: {op}")
                steps.append(f"({op} {left_val} {right_val}) = {result}")
                return result

        result = evaluate(parsed_body, env)
        return result, steps

    return evaluate_step_by_step(parsed_body, {param: arg})


@click.command()
@click.argument("expression", default="λx.x")
@click.argument("argument", type=int, default=1)
def main(expression: str, argument: int):
    """
    Parse and evaluate a lambda expression with a given argument.

    EXPRESSION: The lambda expression as a string.
    ARGUMENT: The integer argument to apply to the lambda expression.
    """
    try:
        result, steps = parse_and_apply_lambda(expression, argument)
        click.echo(f"Expression: {expression}")
        click.echo(f"Argument: {argument}")
        click.echo("Evaluation steps:")
        for step in steps:
            click.echo(f"  {step}")
        click.echo(f"Final result: {result}")
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)


if __name__ == "__main__":
    main()


# Test cases (for demonstration, not part of the CLI)
test_cases = [
    ("λx.(+ x 1)", 2),
    ("λx.((- ((+ x) x)) 3)", 5),
    ("λx.((- ((+ ((* x) x)) ((* 3) x))) 5)", 1),
]

# for i, (expr, arg) in enumerate(test_cases, 1):
#     click.echo(f"\nTest Case {i}:")
#     main.callback(expr, arg)
