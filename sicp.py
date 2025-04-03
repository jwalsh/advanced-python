#!/usr/bin/env python3
"""
Structure and Interpretation of Computer Programs (SICP) Examples
================================================================

This module implements key concepts from SICP in Python,
designed to work well with IPython and Python-mode for
interactive debugging and exploration.

Topics covered:
- Higher-order procedures
- Streams and lazy evaluation
- Environment model
- Metacircular evaluator concepts

When used with Python-mode in Emacs and IPython, you can
step through these implementations to understand their behavior.
"""

from functools import reduce
import math

# Chapter 1: Building Abstractions with Procedures
# ===============================================

# Section 1.1: Higher-order procedures

def sum_integers(a, b):
    """Sum all integers from a through b"""
    if a > b:
        return 0
    return a + sum_integers(a + 1, b)

def sum_cubes(a, b):
    """Sum the cubes of integers from a through b"""
    if a > b:
        return 0
    return a**3 + sum_cubes(a + 1, b)

# Higher-order function version
def sum_iter(term, a, next_fn, b):
    """Sum using iteration instead of recursion"""
    total = 0
    while a <= b:
        total += term(a)
        a = next_fn(a)
    return total

def sum_rec(term, a, next_fn, b):
    """General recursive summation procedure"""
    if a > b:
        return 0
    return term(a) + sum_rec(term, next_fn(a), next_fn, b)

def identity(x):
    return x

def cube(x):
    return x**3

def inc(x):
    return x + 1

# Example usage of higher-order functions
def sum_integers_hof(a, b):
    return sum_rec(identity, a, inc, b)

def sum_cubes_hof(a, b):
    return sum_rec(cube, a, inc, b)

# Section 1.3: Newton's Method
def fixed_point(f, first_guess, tolerance=0.00001):
    """Find a fixed point of function f"""
    def close_enough(v1, v2):
        return abs(v1 - v2) < tolerance
    
    def try_guess(guess):
        next_guess = f(guess)
        if close_enough(guess, next_guess):
            return next_guess
        return try_guess(next_guess)
    
    return try_guess(first_guess)

def sqrt(x):
    """Calculate square root using fixed point"""
    return fixed_point(lambda y: (y + x/y) / 2, 1.0)

def average_damp(f):
    """Average damping function"""
    return lambda x: (x + f(x)) / 2

def sqrt_with_damp(x):
    """Square root with average damping"""
    return fixed_point(average_damp(lambda y: x / y), 1.0)

# Chapter 2: Building Abstractions with Data
# =========================================

# Section 2.1: Data Abstraction
def make_rat(n, d):
    """Create a rational number with numerator n and denominator d"""
    g = math.gcd(n, d)
    return [n // g, d // g]

def numer(x):
    """Get numerator of rational number"""
    return x[0]

def denom(x):
    """Get denominator of rational number"""
    return x[1]

def add_rat(x, y):
    """Add rational numbers"""
    return make_rat(numer(x) * denom(y) + numer(y) * denom(x),
                    denom(x) * denom(y))

def sub_rat(x, y):
    """Subtract rational numbers"""
    return make_rat(numer(x) * denom(y) - numer(y) * denom(x),
                    denom(x) * denom(y))

def mul_rat(x, y):
    """Multiply rational numbers"""
    return make_rat(numer(x) * numer(y), denom(x) * denom(y))

def div_rat(x, y):
    """Divide rational numbers"""
    return make_rat(numer(x) * denom(y), denom(x) * numer(y))

def print_rat(x):
    """Pretty print a rational number"""
    return f"{numer(x)}/{denom(x)}"

# Section 2.2: Hierarchical Data and Closure
def cons(x, y):
    """Construct a pair"""
    return [x, y]

def car(p):
    """Get first element of pair"""
    return p[0]

def cdr(p):
    """Get second element of pair"""
    return p[1]

# List operations using Python lists
def list_ref(items, n):
    """Get the nth item from a list"""
    if n == 0:
        return car(items)
    return list_ref(cdr(items), n - 1)

def map_proc(proc, items):
    """Map procedure over a list"""
    if not items:
        return []
    return [proc(car(items))] + map_proc(proc, cdr(items))

def scale_list(items, factor):
    """Scale each item in a list by a factor"""
    return map_proc(lambda x: x * factor, items)

# Chapter 3: Streams and Lazy Evaluation
# ====================================

# Python implementation of streams using generators
def integers_from(n):
    """Stream of integers from n"""
    while True:
        yield n
        n += 1

def map_stream(proc, stream):
    """Map procedure over a stream"""
    for item in stream:
        yield proc(item)

def filter_stream(pred, stream):
    """Filter stream based on predicate"""
    for item in stream:
        if pred(item):
            yield item

def sieve(stream):
    """Sieve of Eratosthenes as a stream transformer"""
    prime = next(stream)
    yield prime
    yield from sieve(filter_stream(lambda x: x % prime != 0, stream))

def primes():
    """Stream of prime numbers"""
    return sieve(integers_from(2))

# Taking the first n elements of a stream
def take(n, stream):
    """Take first n elements from a stream"""
    result = []
    for _ in range(n):
        try:
            result.append(next(stream))
        except StopIteration:
            break
    return result

# Chapter 4: Metacircular Evaluator (simplified concepts)
# ====================================================

class Environment:
    """Environment implementation for variable lookup"""
    def __init__(self, bindings=None, parent=None):
        self.bindings = bindings or {}
        self.parent = parent
    
    def lookup(self, var):
        """Look up variable in environment"""
        if var in self.bindings:
            return self.bindings[var]
        if self.parent:
            return self.parent.lookup(var)
        raise NameError(f"Variable {var} not found")
    
    def define(self, var, val):
        """Define variable in environment"""
        self.bindings[var] = val
        return val
    
    def set_variable(self, var, val):
        """Set variable value in correct environment"""
        if var in self.bindings:
            self.bindings[var] = val
            return val
        if self.parent:
            return self.parent.set_variable(var, val)
        raise NameError(f"Variable {var} not found")

def make_procedure(parameters, body, env):
    """Create a procedure with given parameters, body, and environment"""
    def execute(*args):
        local_env = Environment({}, env)
        for param, arg in zip(parameters, args):
            local_env.define(param, arg)
        return eval_sequence(body, local_env)
    return execute

def eval_sequence(exprs, env):
    """Evaluate a sequence of expressions"""
    result = None
    for expr in exprs:
        result = evaluate(expr, env)
    return result

def evaluate(expr, env):
    """Simplified evaluator"""
    if isinstance(expr, str):  # Variable
        return env.lookup(expr)
    elif not isinstance(expr, list):  # Self-evaluating
        return expr
    
    # Special forms
    if expr[0] == 'quote':
        return expr[1]
    elif expr[0] == 'if':
        test, consequent, alternative = expr[1], expr[2], expr[3]
        if evaluate(test, env):
            return evaluate(consequent, env)
        else:
            return evaluate(alternative, env)
    elif expr[0] == 'lambda':
        params, body = expr[1], expr[2:]
        return make_procedure(params, body, env)
    elif expr[0] == 'define':
        var, val_expr = expr[1], expr[2]
        val = evaluate(val_expr, env)
        return env.define(var, val)
    elif expr[0] == 'set!':
        var, val_expr = expr[1], expr[2]
        val = evaluate(val_expr, env)
        return env.set_variable(var, val)
    elif expr[0] == 'begin':
        return eval_sequence(expr[1:], env)
    else:  # Procedure application
        procedure = evaluate(expr[0], env)
        args = [evaluate(arg, env) for arg in expr[1:]]
        return procedure(*args)

# Example usage with debugging
if __name__ == "__main__":
    print("Higher-order function demos:")
    print(f"Sum of integers 1 to 10: {sum_integers_hof(1, 10)}")
    print(f"Sum of cubes 1 to 5: {sum_cubes_hof(1, 5)}")
    
    print("\nFixed point demos:")
    print(f"Square root of 2: {sqrt(2)}")
    print(f"Square root of 9: {sqrt_with_damp(9)}")
    
    print("\nRational number demos:")
    one_half = make_rat(1, 2)
    one_third = make_rat(1, 3)
    print(f"1/2 + 1/3 = {print_rat(add_rat(one_half, one_third))}")
    print(f"1/2 * 1/3 = {print_rat(mul_rat(one_half, one_third))}")
    
    print("\nList operation demos:")
    numbers = [1, 2, 3, 4, 5]
    doubled = scale_list(numbers, 2)
    print(f"Doubled list: {doubled}")
    
    print("\nStream demos:")
    print(f"First 10 primes: {take(10, primes())}")
    
    print("\nEnvironment model demos:")
    global_env = Environment({"x": 10, "y": 20})
    local_env = Environment({"y": 30}, global_env)
    print(f"x in local_env: {local_env.lookup('x')}")  # Should find in parent
    print(f"y in local_env: {local_env.lookup('y')}")  # Should find in local
    
    # Example of debugging points in a Python-mode session:
    # import pdb; pdb.set_trace()  # Uncomment for debugging
    
    # Complex calculation to debug
    result = fixed_point(lambda x: math.sin(x) + math.cos(x), 1.0)
    print(f"Fixed point of sin(x) + cos(x): {result}")