#!/bin/bash
# run-lambda-bytecode.sh
# Script to tangle and run the lambda calculus explorer

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Lambda Calculus Bytecode Explorer ===${NC}"
echo -e "${BLUE}===========================================${NC}"

# Check if Emacs is installed
if ! command -v emacs &> /dev/null; then
    echo "Error: Emacs is required for org-mode tangling but it's not installed."
    exit 1
fi

# Source file
ORG_FILE="lambda_calculus_explorer.org"

# Create the org file if not exists
if [ ! -f "$ORG_FILE" ]; then
    echo -e "${BLUE}Creating org-mode file...${NC}"
    cat > "$ORG_FILE" << 'EOF'
#+TITLE: Lambda Calculus and Python Bytecode Explorer
#+AUTHOR: jwalsh
#+DATE: [2025-04-04]
#+PROPERTY: header-args:python :tangle lambda_calculus_explorer.py :mkdirp t

* Lambda Calculus and Python Bytecode Explorer

This project explores the connection between lambda calculus, Python's AST, and bytecode execution.

** 1. Implementation

*** 1.1 Lambda Calculus Parser

#+begin_src python
"""
Lambda Calculus Parser and Interpreter

This module implements a parser and interpreter for a simplified lambda calculus syntax,
translating it to Python bytecode for execution.
"""

import ast
import re
import dis
import types
import inspect
import sys
from pprint import pprint

class LambdaParser:
    """Parser for lambda calculus expressions"""
    
    def __init__(self):
        self.tokens = []
        self.position = 0
    
    def tokenize(self, text):
        """Convert input string to tokens"""
        # Token patterns
        patterns = [
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('LAMBDA', r'lambda'),
            ('COLON', r':'),
            ('IF', r'if'),
            ('THEN', r'then'),
            ('ELSE', r'else'),
            ('RECUR', r'recur'),
            ('NUMBER', r'\d+'),
            ('OPERATOR', r'[\+\-\*/<>=]+'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('COMMA', r','),
            ('WHITESPACE', r'\s+'),
        ]
        
        token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in patterns)
        
        self.tokens = []
        for match in re.finditer(token_regex, text):
            token_type = match.lastgroup
            token_value = match.group()
            
            if token_type != 'WHITESPACE':  # Skip whitespace
                self.tokens.append((token_type, token_value))
        
        self.position = 0
        return self.tokens
    
    def current_token(self):
        """Get the current token"""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None
    
    def next_token(self):
        """Advance to the next token and return it"""
        self.position += 1
        return self.current_token()
    
    def expect(self, token_type):
        """Expect a token of specific type, consume and return it"""
        token = self.current_token()
        if token and token[0] == token_type:
            self.next_token()
            return token
        raise SyntaxError(f"Expected {token_type}, got {token}")
    
    def parse(self, text):
        """Parse a lambda calculus expression and return an AST"""
        self.tokenize(text)
        return self.parse_expression()
    
    def parse_expression(self):
        """Parse an expression"""
        token = self.current_token()
        
        if not token:
            raise SyntaxError("Unexpected end of input")
        
        if token[0] == 'LPAREN':
            # Parse a parenthesized expression or lambda
            self.next_token()  # Consume '('
            
            # Check if it's a lambda
            if self.current_token() and self.current_token()[0] == 'LAMBDA':
                return self.parse_lambda()
            
            # Regular parenthesized expression
            expr = self.parse_expression()
            self.expect('RPAREN')  # Consume ')'
            return expr
            
        elif token[0] == 'LAMBDA':
            # Lambda expression
            return self.parse_lambda()
            
        elif token[0] == 'IF':
            # If expression
            return self.parse_if()
            
        elif token[0] == 'NUMBER':
            # Number literal
            value = int(token[1])
            self.next_token()  # Consume number
            return {'type': 'literal', 'value': value}
            
        elif token[0] == 'IDENTIFIER':
            # Variable reference or function call
            name = token[1]
            self.next_token()  # Consume identifier
            
            # Check if it's a function call
            if self.current_token() and self.current_token()[0] == 'LPAREN':
                return self.parse_function_call(name)
            
            return {'type': 'variable', 'name': name}
            
        elif token[0] == 'RECUR':
            # Recursive call
            self.next_token()  # Consume 'recur'
            
            # Parse arguments
            args = []
            self.expect('LPAREN')
            
            while self.current_token() and self.current_token()[0] != 'RPAREN':
                args.append(self.parse_expression())
                
                # Check for comma separator
                if self.current_token() and self.current_token()[0] == 'COMMA':
                    self.next_token()  # Consume comma
            
            self.expect('RPAREN')  # Consume ')'
            
            return {'type': 'recur', 'args': args}
            
        else:
            raise SyntaxError(f"Unexpected token: {token}")
    
    def parse_lambda(self):
        """Parse a lambda expression"""
        self.next_token()  # Consume 'lambda'
        
        # Parse parameter(s)
        params = []
        
        # Check for opening parenthesis for multiple params
        if self.current_token() and self.current_token()[0] == 'LPAREN':
            self.next_token()  # Consume '('
            
            while self.current_token() and self.current_token()[0] != 'RPAREN':
                param_token = self.expect('IDENTIFIER')
                params.append(param_token[1])
                
                # Check for comma separator
                if self.current_token() and self.current_token()[0] == 'COMMA':
                    self.next_token()  # Consume comma
            
            self.expect('RPAREN')  # Consume ')'
        else:
            # Single parameter
            param_token = self.expect('IDENTIFIER')
            params.append(param_token[1])
        
        # Parse body
        self.expect('COLON')  # Consume ':'
        body = self.parse_expression()
        
        return {
            'type': 'lambda',
            'params': params,
            'body': body
        }
    
    def parse_if(self):
        """Parse an if expression"""
        self.next_token()  # Consume 'if'
        
        condition = self.parse_expression()
        
        self.expect('THEN')  # Consume 'then'
        then_branch = self.parse_expression()
        
        self.expect('ELSE')  # Consume 'else'
        else_branch = self.parse_expression()
        
        return {
            'type': 'if',
            'condition': condition,
            'then': then_branch,
            'else': else_branch
        }
    
    def parse_function_call(self, name):
        """Parse a function call"""
        self.next_token()  # Consume '('
        
        args = []
        while self.current_token() and self.current_token()[0] != 'RPAREN':
            args.append(self.parse_expression())
            
            # Check for comma separator
            if self.current_token() and self.current_token()[0] == 'COMMA':
                self.next_token()  # Consume comma
        
        self.expect('RPAREN')  # Consume ')'
        
        return {
            'type': 'call',
            'function': {'type': 'variable', 'name': name},
            'args': args
        }

class LambdaToAst:
    """Convert lambda calculus AST to Python AST"""
    
    def __init__(self):
        # For tracking recursive functions
        self.recursive_functions = set()
        self.current_function = None
    
    def convert(self, lambda_ast):
        """Convert lambda calculus AST to Python AST"""
        return self.convert_expression(lambda_ast)
    
    def convert_expression(self, expr):
        """Convert an expression from lambda calculus AST to Python AST"""
        expr_type = expr['type']
        
        if expr_type == 'literal':
            return ast.Constant(value=expr['value'])
            
        elif expr_type == 'variable':
            return ast.Name(id=expr['name'], ctx=ast.Load())
            
        elif expr_type == 'lambda':
            # Track current function for recursion
            old_function = self.current_function
            self.current_function = f"lambda_{id(expr)}"
            
            # Convert body
            body_ast = self.convert_expression(expr['body'])
            
            # Check if this function is recursive
            is_recursive = self.current_function in self.recursive_functions
            
            # Create the lambda function
            if is_recursive:
                # For recursive functions, we need to create a wrapper
                # that defines the function with a name and uses Y combinator pattern
                
                # Create parameters
                params = [ast.arg(arg=param, annotation=None) for param in expr['params']]
                
                # Create the function definition
                func_def = ast.FunctionDef(
                    name=self.current_function,
                    args=ast.arguments(
                        posonlyargs=[],
                        args=params,
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[],
                        vararg=None,
                        kwarg=None
                    ),
                    body=[ast.Return(value=body_ast)],
                    decorator_list=[],
                    returns=None
                )
                
                # Create a module to hold the function
                module = ast.Module(
                    body=[func_def, ast.Expr(value=ast.Name(id=self.current_function, ctx=ast.Load()))],
                    type_ignores=[]
                )
                
                # Restore current function
                self.current_function = old_function
                
                return module
            else:
                # Non-recursive lambda is simpler
                lambda_ast = ast.Lambda(
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[ast.arg(arg=param, annotation=None) for param in expr['params']],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[],
                        vararg=None,
                        kwarg=None
                    ),
                    body=body_ast
                )
                
                # Restore current function
                self.current_function = old_function
                
                return lambda_ast
                
        elif expr_type == 'if':
            return ast.IfExp(
                test=self.convert_expression(expr['condition']),
                body=self.convert_expression(expr['then']),
                orelse=self.convert_expression(expr['else'])
            )
            
        elif expr_type == 'call':
            return ast.Call(
                func=self.convert_expression(expr['function']),
                args=[self.convert_expression(arg) for arg in expr['args']],
                keywords=[]
            )
            
        elif expr_type == 'recur':
            # Mark the current function as recursive
            self.recursive_functions.add(self.current_function)
            
            # Create a call to the current function
            return ast.Call(
                func=ast.Name(id=self.current_function, ctx=ast.Load()),
                args=[self.convert_expression(arg) for arg in expr['args']],
                keywords=[]
            )
            
        else:
            raise ValueError(f"Unknown expression type: {expr_type}")

class LambdaInterpreter:
    """Interpreter for lambda calculus expressions"""
    
    def __init__(self):
        self.parser = LambdaParser()
        self.converter = LambdaToAst()
    
    def parse(self, text):
        """Parse lambda calculus expression to internal AST"""
        return self.parser.parse(text)
    
    def convert_to_python_ast(self, lambda_ast):
        """Convert internal AST to Python AST"""
        return self.converter.convert(lambda_ast)
    
    def compile(self, python_ast):
        """Compile Python AST to code object"""
        # Fix missing locations
        ast.fix_missing_locations(python_ast)
        
        # Convert AST to code object
        if isinstance(python_ast, ast.Module):
            code = compile(python_ast, '<lambda>', 'exec')
        else:
            module = ast.Module(body=[ast.Expr(value=python_ast)], type_ignores=[])
            ast.fix_missing_locations(module)
            code = compile(module, '<lambda>', 'eval')
        
        return code
    
    def evaluate(self, text):
        """Evaluate a lambda calculus expression and return the result"""
        # Parse to internal AST
        lambda_ast = self.parse(text)
        print("Internal AST:")
        pprint(lambda_ast)
        
        # Convert to Python AST
        python_ast = self.convert_to_python_ast(lambda_ast)
        print("\nPython AST:")
        print(ast.dump(python_ast, indent=2))
        
        # Compile to code object
        code = self.compile(python_ast)
        
        # Disassemble bytecode
        print("\nBytecode:")
        dis.dis(code)
        
        # Create namespace
        namespace = {}
        
        # Execute or evaluate
        if isinstance(python_ast, ast.Module):
            exec(code, namespace)
            
            # Get the result (the last defined function)
            func_name = list(namespace.keys())[-1]
            result = namespace[func_name]
        else:
            result = eval(code)
        
        return result

def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Lambda Calculus Interpreter")
    parser.add_argument('expression', nargs='?', default=None, help="Lambda calculus expression to evaluate")
    parser.add_argument('--file', '-f', help="Read expression from file")
    parser.add_argument('--test', '-t', action='store_true', help="Run test examples")
    parser.add_argument('--bytecode', '-b', action='store_true', help="Show bytecode details")
    
    args = parser.parse_args()
    
    interpreter = LambdaInterpreter()
    
    if args.test:
        run_tests(interpreter, args.bytecode)
    elif args.file:
        with open(args.file, 'r') as f:
            expression = f.read().strip()
        evaluate_and_test(interpreter, expression, args.bytecode)
    elif args.expression:
        evaluate_and_test(interpreter, args.expression, args.bytecode)
    else:
        # Interactive mode
        print("Lambda Calculus Interpreter")
        print("Enter expressions to evaluate (Ctrl+D to exit)")
        try:
            while True:
                try:
                    expression = input("> ")
                    result = evaluate_and_test(interpreter, expression, args.bytecode)
                except Exception as e:
                    print(f"Error: {e}")
        except EOFError:
            print("\nExiting...")

def run_tests(interpreter, show_bytecode=False):
    """Run test examples"""
    examples = [
        "lambda x: x + 1",
        "lambda (x, y): x + y",
        "lambda n: if n < 2 then 1 else recur(n - 1) + recur(n - 2)",
    ]
    
    for i, example in enumerate(examples):
        print(f"\n\nExample {i+1}: {example}")
        print("-" * 40)
        
        try:
            # Parse and interpret
            result = evaluate_and_test(interpreter, example, show_bytecode)
        except Exception as e:
            print(f"Error: {e}")

def evaluate_and_test(interpreter, expression, show_bytecode=False):
    """Evaluate an expression and test it with sample inputs"""
    # Parse to internal AST
    lambda_ast = interpreter.parse(expression)
    print("Internal AST:")
    pprint(lambda_ast)
    
    # Convert to Python AST
    python_ast = interpreter.convert_to_python_ast(lambda_ast)
    print("\nPython AST:")
    print(ast.dump(python_ast, indent=2))
    
    # Compile to code object
    code = interpreter.compile(python_ast)
    
    if show_bytecode:
        print("\nBytecode:")
        dis.dis(code)
    
    # Create namespace
    namespace = {}
    
    # Execute or evaluate
    if isinstance(python_ast, ast.Module):
        exec(code, namespace)
        
        # Get the result (the last defined function)
        func_name = list(namespace.keys())[-1]
        result = namespace[func_name]
    else:
        result = eval(code)
    
    print("\nResult:", result)
    
    # Test the function if possible
    if callable(result):
        try:
            # Test with example inputs based on the function signature
            if expression.strip().startswith("lambda n:") and "recur" in expression:
                # Fibonacci-like function
                print("\nTesting with sample inputs:")
                for n in range(10):
                    test_result = result(n)
                    print(f"result({n}) = {test_result}")
            elif len(inspect.signature(result).parameters) == 1:
                # Single parameter function
                test_result = result(5)
                print(f"\nTest with input 5: result(5) = {test_result}")
            elif len(inspect.signature(result).parameters) == 2:
                # Two parameter function
                test_result = result(3, 4)
                print(f"\nTest with inputs 3, 4: result(3, 4) = {test_result}")
        except Exception as e:
            print(f"\nError testing function: {e}")
    
    return result

if __name__ == "__main__":
    main()
#+end_src
EOF
fi

# Tangle the org file using emacs
echo -e "${BLUE}Tangling org-mode file...${NC}"
emacs --batch --eval "(require 'org)" --eval "(org-babel-tangle-file \"$ORG_FILE\")"

# Make the Python file executable
chmod +x lambda_calculus_explorer.py

# Run the example
echo -e "${BLUE}\nRunning lambda calculus example...${NC}"
echo -e "${GREEN}./lambda_calculus_explorer.py \"lambda n: if n < 2 then 1 else recur(n - 1) + recur(n - 2)\"${NC}"
./lambda_calculus_explorer.py "lambda n: if n < 2 then 1 else recur(n - 1) + recur(n - 2)"

# Show detailed bytecode
echo -e "${BLUE}\nRunning with detailed bytecode analysis...${NC}"
echo -e "${GREEN}./lambda_calculus_explorer.py -b \"lambda n: if n < 2 then 1 else recur(n - 1) + recur(n - 2)\"${NC}"
./lambda_calculus_explorer.py -b "lambda n: if n < 2 then 1 else recur(n - 1) + recur(n - 2)"

echo -e "\n${BLUE}Done!${NC}"
