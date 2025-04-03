#!/usr/bin/env python3
"""
Lambda Calculus Combinators in Python
====================================

This module implements core combinators from lambda calculus
and demonstrates their usage with Python's support for
higher-order functions.

Key combinators:
- I (identity): λx.x
- K (constant): λx.λy.x
- S (substitution): λx.λy.λz.xz(yz)
- Y (fixed point): λf.(λx.f(xx))(λx.f(xx))

Plus basic list operations (pair, first, rest) in a functional style.

When used in IPython/Python-mode, you can set breakpoints and
inspect the execution flow of these higher-order functions.
"""

# Basic combinators
def I(x):
    """Identity combinator: λx.x"""
    return x

def K(x):
    """Constant combinator: λx.λy.x"""
    def K_inner(y):
        return x
    return K_inner

def S(x):
    """Substitution combinator: λx.λy.λz.xz(yz)"""
    def S_y(y):
        def S_z(z):
            return x(z)(y(z))
        return S_z
    return S_y

# Y combinator (fixed point combinator)
def Y(f):
    """
    Y combinator: λf.(λx.f(xx))(λx.f(xx))
    
    Note: In Python this direct implementation would cause
    infinite recursion immediately due to eager evaluation.
    This is a modified version that works in Python.
    """
    def g(h):
        return lambda *args: f(h(h))(*args)
    return g(g)

# Functional pair implementation
def pair(first, rest):
    """Create a pair: λx.λy.λf.fxy"""
    def pair_inner(selector):
        return selector(first, rest)
    return pair_inner

def first(p):
    """Get the first element of a pair: λp.p(λx.λy.x)"""
    return p(lambda x, y: x)

def rest(p):
    """Get the rest element of a pair: λp.p(λx.λy.y)"""
    return p(lambda x, y: y)

# Example of a list using pairs
def make_list(*elements):
    """Create a list from elements using pairs"""
    result = None
    for element in reversed(elements):
        result = pair(element, result)
    return result

def map_list(func, lst):
    """Map a function over a list implemented as pairs"""
    if lst is None:
        return None
    return pair(func(first(lst)), map_list(func, rest(lst)))

def filter_list(predicate, lst):
    """Filter a list implemented as pairs"""
    if lst is None:
        return None
    
    head = first(lst)
    tail = rest(lst)
    
    if predicate(head):
        return pair(head, filter_list(predicate, tail))
    else:
        return filter_list(predicate, tail)

def to_python_list(lst):
    """Convert our functional list to a Python list"""
    result = []
    current = lst
    
    while current is not None:
        result.append(first(current))
        current = rest(current)
    
    return result

# Demonstration with factorial using Y combinator
def factorial_gen(f):
    def factorial(n):
        if n == 0:
            return 1
        else:
            return n * f(n-1)
    return factorial

factorial = Y(factorial_gen)

# Demo code with debugging examples
if __name__ == "__main__":
    # Test basic combinators
    print("I(5) =", I(5))
    print("K(3)(7) =", K(3)(7))
    
    # Test functional pairs
    p = pair(1, 2)
    print("pair(1, 2):", first(p), rest(p))
    
    # Test list operations
    numbers = make_list(1, 2, 3, 4, 5)
    doubled = map_list(lambda x: x * 2, numbers)
    evens = filter_list(lambda x: x % 2 == 0, numbers)
    
    print("Original list:", to_python_list(numbers))
    print("Doubled:", to_python_list(doubled))
    print("Evens:", to_python_list(evens))
    
    # Test factorial using Y combinator
    for i in range(6):
        print(f"factorial({i}) = {factorial(i)}")
    
    # Example of how to use breakpoints in IPython/Python-mode
    # In Python-mode: Set breakpoint at this line and step through
    # import pdb; pdb.set_trace()  # Uncomment for manual debugging
    print("Factorial using Y combinator:", factorial(5))