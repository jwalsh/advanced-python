# bytecode_inspector.py

import py_compile
import dis
import os
import marshal
import importlib.util
import argparse
from pathlib import Path

def compile_to_bytecode(file_path):
    """Compile a Python file to bytecode and return the path to the .pyc file"""
    try:
        py_compile.compile(file_path)
        print(f"Successfully compiled {file_path}")
        
        # Find the compiled .pyc file
        cache_dir = '__pycache__'
        base_name = os.path.basename(file_path)
        module_name = os.path.splitext(base_name)[0]
        
        if os.path.exists(cache_dir):
            pyc_files = [f for f in os.listdir(cache_dir) if f.startswith(f"{module_name}.")]
            if pyc_files:
                return os.path.join(cache_dir, pyc_files[0])
    except Exception as e:
        print(f"Error compiling {file_path}: {e}")
    
    return None

def inspect_bytecode(pyc_path):
    """Disassemble and inspect a .pyc file"""
    if not pyc_path or not os.path.exists(pyc_path):
        print("No valid .pyc file found")
        return
    
    try:
        # Load the module from the .pyc file
        spec = importlib.util.spec_from_file_location("module.name", pyc_path)
        if spec:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Print all functions/classes and their bytecode
            for name, obj in module.__dict__.items():
                if callable(obj) and not name.startswith('__'):
                    print(f"\n{'='*50}")
                    print(f"Disassembly of {name}:")
                    print(f"{'='*50}")
                    dis.dis(obj)
        
        # Directly examine the bytecode
        print(f"\n{'='*50}")
        print(f"Raw bytecode from {pyc_path}:")
        print(f"{'='*50}")
        with open(pyc_path, 'rb') as pyc_file:
            # Skip the magic number and timestamp/size
            pyc_file.read(16)  # 4 bytes magic + 4 bytes timestamp + 4 bytes size + 4 bytes hash
            
            # Load the code object
            try:
                code_obj = marshal.load(pyc_file)
                dis.dis(code_obj)
            except Exception as e:
                print(f"Error loading code object: {e}")
                
    except Exception as e:
        print(f"Error inspecting {pyc_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Compile Python files to bytecode and inspect them')
    parser.add_argument('file', help='Python file to compile and inspect')
    parser.add_argument('--no-compile', action='store_true', 
                        help='Inspect existing .pyc without recompiling')
    
    args = parser.parse_args()
    
    file_path = args.file
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    if args.no_compile:
        # Try to find existing .pyc file
        cache_dir = '__pycache__'
        base_name = os.path.basename(file_path)
        module_name = os.path.splitext(base_name)[0]
        
        if os.path.exists(cache_dir):
            pyc_files = [f for f in os.listdir(cache_dir) if f.startswith(f"{module_name}.")]
            if pyc_files:
                pyc_path = os.path.join(cache_dir, pyc_files[0])
                print(f"Using existing .pyc file: {pyc_path}")
                inspect_bytecode(pyc_path)
            else:
                print(f"No existing .pyc file found for {file_path}")
    else:
        pyc_path = compile_to_bytecode(file_path)
        if pyc_path:
            print(f"Compiled to: {pyc_path}")
            inspect_bytecode(pyc_path)

if __name__ == "__main__":
    main()
