#!/usr/bin/env python3
"""
A Simple Reflective Tower Interpreter
====================================

Inspired by the Black interpreter and reflective towers concept
(https://github.com/readevalprintlove/black).

This implements a meta-circular evaluator with reflection capabilities,
designed for interactive debugging with IPython/Python-mode.

Core concepts:
- Base evaluator (eval-apply)
- Environments and closures
- Reflection - ability to modify the evaluator during execution
- Tower structure - interpreters interpreting interpreters

This is a simplified Python implementation that focuses on the core
concepts while being amenable to step-by-step debugging.
"""

import sys
from enum import Enum, auto
from functools import reduce


# Token types for our simple language
class TokenType(Enum):
    NUMBER = auto()
    SYMBOL = auto()
    STRING = auto()
    LPAREN = auto()
    RPAREN = auto()
    QUOTE = auto()
    EOF = auto()


class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return f"Token({self.type}, {repr(self.value)})"
        return f"Token({self.type})"


class Lexer:
    """Simple lexer for our language"""

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        """Advance the position pointer"""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """Skip whitespace characters"""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        """Skip comment lines"""
        while self.current_char is not None and self.current_char != "\n":
            self.advance()
        self.advance()  # Skip the newline

    def number(self):
        """Process a number token"""
        result = ""
        while self.current_char is not None and (
            self.current_char.isdigit() or self.current_char == "."
        ):
            result += self.current_char
            self.advance()

        try:
            if "." in result:
                return Token(TokenType.NUMBER, float(result))
            else:
                return Token(TokenType.NUMBER, int(result))
        except ValueError:
            raise Exception(f"Invalid number: {result}")

    def string(self):
        """Process a string token"""
        result = ""
        self.advance()  # Skip opening quote
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == "\\":
                self.advance()
                if self.current_char == "n":
                    result += "\n"
                elif self.current_char == "t":
                    result += "\t"
                else:
                    result += self.current_char
            else:
                result += self.current_char
            self.advance()

        if self.current_char is None:
            raise Exception("Unterminated string")

        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, result)

    def symbol(self):
        """Process a symbol token"""
        result = ""
        while (
            self.current_char is not None
            and not self.current_char.isspace()
            and self.current_char not in "()'"
        ):
            result += self.current_char
            self.advance()
        return Token(TokenType.SYMBOL, result)

    def get_next_token(self):
        """Get the next token from the input"""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == ";":
                self.skip_comment()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == '"':
                return self.string()

            if self.current_char == "(":
                self.advance()
                return Token(TokenType.LPAREN)

            if self.current_char == ")":
                self.advance()
                return Token(TokenType.RPAREN)

            if self.current_char == "'":
                self.advance()
                return Token(TokenType.QUOTE)

            # Must be a symbol
            return self.symbol()

        return Token(TokenType.EOF)


class Parser:
    """Simple parser for our language"""

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message):
        raise Exception(f"Parser error: {message}")

    def eat(self, token_type):
        """Consume the current token if it matches the expected type"""
        if self.current_token.type == token_type:
            result = self.current_token
            self.current_token = self.lexer.get_next_token()
            return result
        else:
            self.error(f"Expected {token_type}, got {self.current_token.type}")

    def parse(self):
        """Parse the input and return an AST"""
        if self.current_token.type == TokenType.EOF:
            return None

        return self.expression()

    def expression(self):
        """Parse an expression"""
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return token.value

        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return token.value

        elif token.type == TokenType.SYMBOL:
            self.eat(TokenType.SYMBOL)
            return Symbol(token.value)

        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            result = []

            while self.current_token.type != TokenType.RPAREN:
                result.append(self.expression())

                if self.current_token.type == TokenType.EOF:
                    self.error("Unexpected end of input, expected ')'")

            self.eat(TokenType.RPAREN)
            return result

        elif token.type == TokenType.QUOTE:
            self.eat(TokenType.QUOTE)
            return [Symbol("quote"), self.expression()]

        else:
            self.error(f"Unexpected token: {token}")


class Symbol:
    """Symbol class for our language"""

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name


class Environment:
    """Environment for variable bindings"""

    def __init__(self, params=(), args=(), outer=None):
        self.bindings = dict(zip(params, args))
        self.outer = outer

    def lookup(self, symbol):
        """Look up a symbol in the environment"""
        if symbol in self.bindings:
            return self.bindings[symbol]
        if self.outer:
            return self.outer.lookup(symbol)
        raise Exception(f"Undefined symbol: {symbol}")

    def define(self, symbol, value):
        """Define a new binding in the environment"""
        self.bindings[symbol] = value
        return value

    def set(self, symbol, value):
        """Set an existing binding in the environment"""
        if symbol in self.bindings:
            self.bindings[symbol] = value
            return value
        if self.outer:
            return self.outer.set(symbol, value)
        raise Exception(f"Undefined symbol: {symbol}")


class Procedure:
    """User-defined procedure"""

    def __init__(self, params, body, env, evaluator=None):
        self.params = params
        self.body = body
        self.env = env
        self.evaluator = evaluator  # For tower reflection

    def __call__(self, *args):
        # Create new environment extending the procedure's environment
        if self.evaluator:
            # Use the procedure's own evaluator (reflective tower)
            return self.evaluator.eval_sequence(
                self.body, Environment([p.name for p in self.params], args, self.env)
            )
        else:
            # Use the current evaluator
            return eval_sequence(
                self.body, Environment([p.name for p in self.params], args, self.env)
            )


class Evaluator:
    """Meta-circular evaluator with reflection capabilities"""

    def __init__(self, global_env=None, meta_evaluator=None):
        self.global_env = global_env if global_env else self.make_global_env()
        self.meta_evaluator = meta_evaluator  # Higher level evaluator (for towers)

    def make_global_env(self):
        """Create the global environment with primitive procedures"""
        env = Environment()

        # Arithmetic operations
        env.define(Symbol("+"), lambda *args: sum(args))
        env.define(Symbol("-"), lambda x, *args: x - sum(args) if args else -x)
        env.define(Symbol("*"), lambda *args: reduce(lambda x, y: x * y, args, 1))
        env.define(
            Symbol("/"),
            lambda x, *args: x / reduce(lambda y, z: y * z, args, 1) if args else 1 / x,
        )

        # Comparison operations
        env.define(Symbol("="), lambda x, y: x == y)
        env.define(Symbol("<"), lambda x, y: x < y)
        env.define(Symbol(">"), lambda x, y: x > y)
        env.define(Symbol("<="), lambda x, y: x <= y)
        env.define(Symbol(">="), lambda x, y: x >= y)

        # List operations
        env.define(
            Symbol("cons"), lambda x, y: [x] + (y if isinstance(y, list) else [y])
        )
        env.define(Symbol("car"), lambda x: x[0])
        env.define(Symbol("cdr"), lambda x: x[1:])
        env.define(Symbol("list"), lambda *args: list(args))
        env.define(
            Symbol("null?"), lambda x: len(x) == 0 if isinstance(x, list) else False
        )

        # Type checking
        env.define(Symbol("number?"), lambda x: isinstance(x, (int, float)))
        env.define(Symbol("symbol?"), lambda x: isinstance(x, Symbol))
        env.define(Symbol("string?"), lambda x: isinstance(x, str))
        env.define(Symbol("procedure?"), lambda x: callable(x))

        # Display
        env.define(Symbol("display"), lambda x: print(x, end=""))
        env.define(Symbol("newline"), lambda: print())

        # Reflection capabilities
        env.define(
            Symbol("eval"),
            lambda x, env=None: self.eval(x, env if env else self.global_env),
        )
        env.define(Symbol("apply"), lambda proc, args: proc(*args))

        # Tower operations
        env.define(
            Symbol("make-evaluator"),
            lambda: Evaluator(Environment(outer=self.global_env), self),
        )

        return env

    def eval(self, expr, env):
        """Evaluate an expression in an environment"""
        # Self-evaluating expressions
        if isinstance(expr, (int, float, str)):
            return expr

        # Variable reference
        if isinstance(expr, Symbol):
            return env.lookup(expr)

        # Special forms
        if isinstance(expr, list) and len(expr) > 0:
            op = expr[0]

            # Quote
            if op == Symbol("quote"):
                return expr[1]

            # If conditional
            elif op == Symbol("if"):
                test, conseq, alt = expr[1], expr[2], expr[3] if len(expr) > 3 else None
                if self.eval(test, env):
                    return self.eval(conseq, env)
                elif alt:
                    return self.eval(alt, env)
                else:
                    return None

            # Definition
            elif op == Symbol("define"):
                if isinstance(expr[1], Symbol):
                    # Variable definition
                    return env.define(expr[1], self.eval(expr[2], env))
                else:
                    # Procedure definition
                    name = expr[1][0]
                    params = expr[1][1:]
                    body = expr[2:]
                    return env.define(name, Procedure(params, body, env, self))

            # Assignment
            elif op == Symbol("set!"):
                return env.set(expr[1], self.eval(expr[2], env))

            # Lambda expression
            elif op == Symbol("lambda"):
                params = expr[1]
                body = expr[2:]
                return Procedure(params, body, env, self)

            # Begin (sequence)
            elif op == Symbol("begin"):
                return self.eval_sequence(expr[1:], env)

            # Let (local bindings)
            elif op == Symbol("let"):
                bindings = expr[1]
                body = expr[2:]

                # Create new environment for let
                let_env = Environment(outer=env)

                # Evaluate bindings
                for binding in bindings:
                    var, val_expr = binding[0], binding[1]
                    let_env.define(var, self.eval(val_expr, env))

                # Evaluate body in new environment
                return self.eval_sequence(body, let_env)

            # Procedure application
            else:
                procedure = self.eval(op, env)
                arguments = [self.eval(arg, env) for arg in expr[1:]]
                return self.apply(procedure, arguments)

        raise Exception(f"Invalid expression: {expr}")

    def eval_sequence(self, exprs, env):
        """Evaluate a sequence of expressions"""
        result = None
        for expr in exprs:
            result = self.eval(expr, env)
        return result

    def apply(self, procedure, arguments):
        """Apply a procedure to arguments"""
        if isinstance(procedure, Procedure):
            return procedure(*arguments)
        elif callable(procedure):
            return procedure(*arguments)
        else:
            raise Exception(f"Cannot apply {procedure}")


def read(source):
    """Read a source string and parse it"""
    lexer = Lexer(source)
    parser = Parser(lexer)
    return parser.parse()


def evaluate(expr, env=None):
    """Evaluate an expression in an environment"""
    evaluator = Evaluator()
    if env is None:
        env = evaluator.global_env
    return evaluator.eval(expr, env)


def repl():
    """Run a read-eval-print loop"""
    evaluator = Evaluator()
    env = evaluator.global_env

    print("Reflective Tower Interpreter")
    print("Type 'exit' to quit")

    while True:
        try:
            source = input("> ")
            if source.lower() == "exit":
                break

            expr = read(source)
            if expr is not None:
                result = evaluator.eval(expr, env)
                print("=>", result)
        except Exception as e:
            print("Error:", e)


# Demo code to show the reflective tower in action
if __name__ == "__main__":
    # Run REPL if no arguments provided
    if len(sys.argv) == 1:
        repl()
    # Otherwise, evaluate the file
    else:
        with open(sys.argv[1], "r") as f:
            source = f.read()

        try:
            expr = read(source)
            evaluator = Evaluator()
            result = evaluator.eval(expr, evaluator.global_env)
            print("=>", result)
        except Exception as e:
            print("Error:", e)
