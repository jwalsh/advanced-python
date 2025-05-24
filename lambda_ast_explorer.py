# lambda_ast_explorer.py

import ast
import inspect
import types
import dis
import textwrap
from pprint import pprint

# Basic lambda calculus implementation
def pair(x, y):
    """Create a pair that holds two values together"""
    return lambda selector: selector(x, y)

def first(p):
    """Extract the first element from a pair"""
    return p(lambda x, y: x)

def rest(p):
    """Extract the second element from a pair"""
    return p(lambda x, y: y)

def make_list(*elements):
    """Construct a list from elements in lambda calculus style"""
    if not elements:
        return None  # Empty list
    if len(elements) == 1:
        return pair(elements[0], None)  # Single element list
    return pair(elements[0], make_list(*elements[1:]))  # Recursive list construction

def print_list(lst):
    """Print a lambda calculus style list"""
    result = []
    current = lst
    while current is not None:
        if callable(current) and isinstance(current, types.LambdaType):
            # It's a pair
            result.append(first(current))
            current = rest(current)
        else:
            # It's a regular value
            result.append(current)
            current = None
    return result

def explore_ast(source_code):
    """Parse Python code into an AST and display its structure"""
    print(f"\n{'='*60}")
    print(f"AST for: {source_code}")
    print(f"{'='*60}")
    
    # Parse the source code into an AST
    parsed_ast = ast.parse(source_code)
    
    # Pretty print the AST 
    print("Raw AST structure:")
    for node in ast.walk(parsed_ast):
        print(f"{type(node).__name__}: {ast.dump(node)}")
    
    # Compile and execute the code
    compiled_code = compile(parsed_ast, '<string>', 'exec')
    local_vars = {}
    global_vars = globals().copy()
    
    print("\nExecuting code and inspecting bytecode...")
    exec(compiled_code, global_vars, local_vars)
    
    # Find the functions or expressions to disassemble
    for name, obj in local_vars.items():
        if callable(obj):
            print(f"\nDisassembly of {name}:")
            dis.dis(obj)
            
            # If it's a lambda function, show more details
            if isinstance(obj, types.LambdaType):
                print(f"\nLambda function details:")
                print(f"  Name: {obj.__name__}")
                print(f"  Code: {inspect.getsource(obj)}")
                print(f"  Closure: {obj.__closure__}")
                
                # Try to evaluate it for demonstration
                try:
                    if name.startswith('list_'):
                        print(f"  Evaluation: {print_list(obj)}")
                except Exception as e:
                    print(f"  Error evaluating: {e}")
    
    return local_vars

if __name__ == "__main__":
    # Example 1: Simple pair
    example1 = """
p = pair(1, 2)
f = first(p)
r = rest(p)
"""
    result1 = explore_ast(example1)
    
    # Example 2: List construction
    example2 = """
list_123 = make_list(1, 2, 3)
list_nested = make_list(1, 2, 3, make_list(4, 5))
"""
    result2 = explore_ast(example2)
    
    # Example 3: Custom lambda expressions
    example3 = """
identity = lambda x: x
compose = lambda f, g: lambda x: f(g(x))
twice = lambda f: lambda x: f(f(x))
"""
    result3 = explore_ast(example3)
    
    # Example 4: User-defined input
    print("\n\nEnter your own lambda calculus expression to analyze:")
    user_code = input("> ")
    if user_code:
        result4 = explore_ast(user_code)
