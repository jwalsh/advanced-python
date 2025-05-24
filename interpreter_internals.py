#!/usr/bin/env python3
"""
Python Interpreter Internals Explorer

This script explores the internal structures and mechanisms of Python interpreters
including CPython and IPython, focusing on:
- Memory management and object structures
- Frame objects and execution model
- Interpreter state and thread state
- Extension module interfaces
- Evaluation loop
"""

import sys
import os
import inspect
import types
import ctypes
import gc
import dis
import marshal
import importlib
import importlib.util
import traceback
from pprint import pprint

# Check if IPython is available
try:
    import IPython
    IPYTHON_AVAILABLE = True
except ImportError:
    IPYTHON_AVAILABLE = False

class PythonInternalsExplorer:
    """
    Explorer for Python interpreter internals
    """
    
    def __init__(self):
        self.python_version = sys.version
        self.implementation = sys.implementation.name
        self.interpreter_path = sys.executable
        
    def print_separator(self, title):
        """Print a section separator with title"""
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}")
        
    def explore_interpreter_info(self):
        """Display basic information about the Python interpreter"""
        self.print_separator("Python Interpreter Information")
        print(f"Python Version: {self.python_version}")
        print(f"Implementation: {self.implementation}")
        print(f"Executable Path: {self.interpreter_path}")
        print(f"Compiled with: {sys.implementation.cache_tag}")
        print(f"Flags: {sys.flags}")
        print(f"Check Interval: {sys.getcheckinterval()}")
        print(f"Thread Switch Interval: {sys.getswitchinterval()}")
        
        # Python memory info
        print("\nMemory Information:")
        try:
            import resource
            print(f"Resource usage: {resource.getrusage(resource.RUSAGE_SELF)}")
        except ImportError:
            print("Resource module not available")
            
        # Python paths
        print("\nPath Information:")
        print(f"Module Search Paths: {sys.path}")
        print(f"Executable Path: {sys.executable}")
        print(f"Platform: {sys.platform}")
        
    def explore_memory_management(self):
        """Explore Python memory management internals"""
        self.print_separator("Memory Management")
        
        # Create and track some objects
        sample_objects = [
            42,  # int
            "hello",  # str
            [1, 2, 3],  # list
            {"a": 1, "b": 2},  # dict
            lambda x: x*2,  # function
        ]
        
        print("Object Structure Examples:")
        for obj in sample_objects:
            print(f"\nObject of type {type(obj).__name__}:")
            print(f"  ID: {id(obj)}")
            print(f"  Size: {sys.getsizeof(obj)} bytes")
            print(f"  Reference count: {sys.getrefcount(obj) - 1}")  # -1 for the reference in this function
            print(f"  Memory address: {hex(id(obj))}")
            if hasattr(obj, "__dict__"):
                print(f"  Attributes: {obj.__dict__}")
                
        # Memory allocations
        print("\nGarbage Collection Information:")
        print(f"  GC enabled: {gc.isenabled()}")
        print(f"  GC thresholds: {gc.get_threshold()}")
        print(f"  Current GC counts: {gc.get_count()}")
        print(f"  Objects tracked by GC: {len(gc.get_objects())}")
        
    def explore_code_objects(self):
        """Explore code objects and function internals"""
        self.print_separator("Code Objects and Function Internals")
        
        # Define a sample function to explore
        def sample_function(a, b=10, *args, **kwargs):
            """A sample function to explore"""
            x = a + b
            for i in args:
                x += i
            for k, v in kwargs.items():
                if isinstance(v, int):
                    x += v
            return x
        
        # Get function's code object
        code = sample_function.__code__
        
        print("Function details:")
        print(f"  Name: {sample_function.__name__}")
        print(f"  Defaults: {sample_function.__defaults__}")
        print(f"  Closure: {sample_function.__closure__}")
        print(f"  Module: {sample_function.__module__}")
        print(f"  Annotations: {sample_function.__annotations__}")
        
        print("\nCode object details:")
        print(f"  Filename: {code.co_filename}")
        print(f"  Name: {code.co_name}")
        print(f"  Argument count: {code.co_argcount}")
        print(f"  Positional-only arguments: {code.co_posonlyargcount}")
        print(f"  Keyword-only arguments: {code.co_kwonlyargcount}")
        print(f"  Number of locals: {code.co_nlocals}")
        print(f"  Stack size: {code.co_stacksize}")
        print(f"  Flags: {code.co_flags}")
        print(f"  Constants: {code.co_consts}")
        print(f"  Names: {code.co_names}")
        print(f"  Variable names: {code.co_varnames}")
        print(f"  Free variables: {code.co_freevars}")
        print(f"  Cell variables: {code.co_cellvars}")
        
        # Disassemble the function
        print("\nBytecode disassembly:")
        dis.dis(sample_function)
        
    def explore_frame_objects(self):
        """Explore frame objects and execution model"""
        self.print_separator("Frame Objects and Execution Model")
        
        # Function to examine its own frame
        def frame_inspector():
            current_frame = sys._getframe()
            caller_frame = current_frame.f_back
            
            print("Current frame details:")
            print(f"  Code: {current_frame.f_code.co_name}")
            print(f"  Line number: {current_frame.f_lineno}")
            print(f"  Locals: {current_frame.f_locals.keys()}")
            print(f"  Globals: {list(current_frame.f_globals.keys())[:10]}...")
            print(f"  Built-ins: {list(current_frame.f_builtins.keys())[:10]}...")
            
            if caller_frame:
                print("\nCaller frame details:")
                print(f"  Code: {caller_frame.f_code.co_name}")
                print(f"  Line number: {caller_frame.f_lineno}")
                
            # Print the call stack
            print("\nCall stack:")
            for frame_info in inspect.stack():
                print(f"  {frame_info.function} at {frame_info.filename}:{frame_info.lineno}")
                
        # Call the frame inspector
        frame_inspector()
        
    def explore_interpreter_state(self):
        """Explore the interpreter state and thread state"""
        self.print_separator("Interpreter State and Thread State")
        
        print("Thread State Information:")
        print(f"  Current thread: {threading.current_thread().name}")
        print(f"  Thread count: {threading.active_count()}")
        print(f"  Thread identifiers: {[t.ident for t in threading.enumerate()]}")
        
        print("\nInterpreter Internals (limited access in pure Python):")
        print(f"  Check interval: {sys.getcheckinterval()}")
        print(f"  Switch interval: {sys.getswitchinterval()}")
        print(f"  Default encoding: {sys.getdefaultencoding()}")
        print(f"  File system encoding: {sys.getfilesystemencoding()}")
        
        # This would require C extension modules to fully explore
        print("\nNote: For deeper interpreter state inspection, C extension modules are needed")
        
    def explore_extension_modules(self):
        """Explore Python's C API and extension modules"""
        self.print_separator("C API and Extension Modules")
        
        # List built-in modules
        print("Built-in modules:")
        for name in sorted(sys.builtin_module_names):
            print(f"  {name}")
            
        # Check for common extension modules
        extension_modules = ['ctypes', 'numpy', 'pandas', '_socket', '_ssl']
        print("\nExtension module examples:")
        for module_name in extension_modules:
            try:
                module = importlib.import_module(module_name)
                file_path = getattr(module, '__file__', 'Built-in')
                print(f"  {module_name}: {file_path}")
            except ImportError:
                print(f"  {module_name}: Not available")
                
        print("\nCtypes for interfacing with C:")
        try:
            # Example using ctypes to access C functionality
            if sys.platform == 'win32':
                libc = ctypes.cdll.msvcrt
            elif sys.platform == 'darwin':
                libc = ctypes.cdll.LoadLibrary('libc.dylib')
            else:
                libc = ctypes.cdll.LoadLibrary('libc.so.6')
                
            print(f"  Loaded libc: {libc}")
            print(f"  Address of printf: {libc.printf}")
        except Exception as e:
            print(f"  Error loading libc: {e}")
            
    def explore_ipython_integration(self):
        """Explore IPython specific internals"""
        self.print_separator("IPython Integration")
        
        if not IPYTHON_AVAILABLE:
            print("IPython is not available in this environment.")
            return
            
        print("IPython Information:")
        print(f"  IPython version: {IPython.__version__}")
        print(f"  IPython path: {IPython.__file__}")
        
        # Check if running in IPython
        is_ipython = False
        try:
            __IPYTHON__
            is_ipython = True
        except NameError:
            pass
            
        print(f"  Running in IPython: {is_ipython}")
        
        if is_ipython:
            print("\nIPython Configuration:")
            ip = get_ipython()
            print(f"  Profile: {ip.profile}")
            print(f"  User namespace: {list(ip.user_ns_hidden)[:10]}...")
            print(f"  Magic functions: {list(ip.magics_manager.magics['line'].keys())[:10]}...")
            
        # Print IPython extension mechanism
        print("\nIPython Extension System:")
        print("  Extensions provide additional functionality to IPython")
        print("  Examples: %autoreload, %matplotlib, etc.")
        
    def explore_bytecode_execution(self):
        """Explore bytecode execution and VM operations"""
        self.print_separator("Bytecode Execution and VM Operations")
        
        # Define a simple function to explore
        def fib(n):
            a, b = 0, 1
            for i in range(n):
                a, b = b, a + b
            return a
        
        # Explore bytecode
        print("Bytecode for Fibonacci function:")
        dis.dis(fib)
        
        # Get code object
        code = fib.__code__
        
        # Examine the const pool
        print("\nConstants pool:")
        for i, const in enumerate(code.co_consts):
            print(f"  [{i}] {const} ({type(const).__name__})")
        
        # Examine names
        print("\nNames:")
        for i, name in enumerate(code.co_names):
            print(f"  [{i}] {name}")
        
        # Examine variable names
        print("\nVariable names:")
        for i, var in enumerate(code.co_varnames):
            print(f"  [{i}] {var}")
        
        # Create a .pyc file to examine
        import tempfile
        import marshal
        
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
            f.write(b'def example(): return 42\n')
            temp_filename = f.name
            
        # Compile to .pyc
        import py_compile
        py_compile.compile(temp_filename)
        
        # Find the .pyc file
        pyc_file = None
        cache_dir = os.path.join(os.path.dirname(temp_filename), '__pycache__')
        if os.path.exists(cache_dir):
            for filename in os.listdir(cache_dir):
                if filename.startswith(os.path.basename(temp_filename)):
                    pyc_file = os.path.join(cache_dir, filename)
                    break
        
        if pyc_file:
            print(f"\nExamining .pyc file: {pyc_file}")
            with open(pyc_file, 'rb') as f:
                # Read and parse .pyc header
                magic = f.read(4)
                bit_field = f.read(4)  # PEP 552 - bit field for file hash
                source_size = f.read(4)  # Size of source code
                source_hash = f.read(4)  # Hash of source code
                
                print(f"  Magic number: {magic.hex()}")
                print(f"  Bit field: {bit_field.hex()}")
                print(f"  Source size: {int.from_bytes(source_size, byteorder='little')}")
                print(f"  Source hash: {source_hash.hex()}")
                
                # Load code object
                try:
                    code_obj = marshal.load(f)
                    print("\n  Code object loaded successfully")
                    print(f"  Code object type: {type(code_obj)}")
                    print(f"  Function name: {code_obj.co_name}")
                    print(f"  Bytecode: {code_obj.co_code.hex()}")
                except Exception as e:
                    print(f"  Error loading code object: {e}")
        
        # Clean up
        try:
            os.unlink(temp_filename)
            if pyc_file:
                os.unlink(pyc_file)
        except:
            pass
        
    def explore_all(self):
        """Run all exploration functions"""
        self.explore_interpreter_info()
        self.explore_memory_management()
        self.explore_code_objects()
        self.explore_frame_objects()
        
        # These explorations may require additional setup
        try:
            import threading
            self.explore_interpreter_state()
        except ImportError:
            self.print_separator("Interpreter State - SKIPPED (threading module not available)")
        
        self.explore_extension_modules()
        
        if IPYTHON_AVAILABLE:
            self.explore_ipython_integration()
        else:
            self.print_separator("IPython Integration - SKIPPED (IPython not available)")
            
        self.explore_bytecode_execution()
        
        self.print_separator("Exploration Complete")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Explore Python interpreter internals")
    parser.add_argument('--section', choices=[
        'info', 'memory', 'code', 'frame', 'state', 
        'extensions', 'ipython', 'bytecode', 'all'
    ], default='all', help="Specific section to explore")
    
    args = parser.parse_args()
    
    explorer = PythonInternalsExplorer()
    
    if args.section == 'info':
        explorer.explore_interpreter_info()
    elif args.section == 'memory':
        explorer.explore_memory_management()
    elif args.section == 'code':
        explorer.explore_code_objects()
    elif args.section == 'frame':
        explorer.explore_frame_objects()
    elif args.section == 'state':
        import threading
        explorer.explore_interpreter_state()
    elif args.section == 'extensions':
        explorer.explore_extension_modules()
    elif args.section == 'ipython':
        explorer.explore_ipython_integration()
    elif args.section == 'bytecode':
        explorer.explore_bytecode_execution()
    else:
        explorer.explore_all()
