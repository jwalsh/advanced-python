# Context Managers Exercise

# In this exercise, you'll be implementing a context manager to manage the opening and closing of a file.
# The context manager will automatically close the file when the 'with' block is exited, even if an exception occurs.

# Problem:
# You have a file named "data.txt" that contains some text data. Your task is to create a context manager
# named 'FileManager' that opens the file, allows reading its contents, and automatically closes the file
# when the 'with' block is exited.

# Step 1: Implement the FileManager context manager
# - Create a class named 'FileManager' that acts as a context manager.
# - Implement the '__init__' method to initialize the context manager with the file path.
# - Implement the '__enter__' method to open the file and return the file object.
# - Implement the '__exit__' method to close the file when the 'with' block is exited.

# Step 2: Use the FileManager context manager
# - Use the 'with' statement along with the 'FileManager' context manager to open the file.
# - Read the contents of the file using the 'read' method.
# - Print the contents of the file.

# Example usage:
# with FileManager("data.txt") as file:
#     contents = file.read()
#     print(contents)

# Assume the contents of "data.txt" are:
# This is a sample file.
# It contains some text data.
# We'll use a context manager to manage the file.

# Expected output:
# This is a sample file.
# It contains some text data.
# We'll use a context manager to manage the file.

# Explanation:
# The 'FileManager' context manager takes care of opening the file in the '__enter__' method and closing it
# in the '__exit__' method. By using the 'with' statement, we ensure that the file is properly closed, even
# if an exception occurs within the 'with' block. This helps in resource management and prevents leaks.

# Note: Make sure to create a file named "data.txt" with the example contents before running the code.
