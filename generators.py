# Generators Exercise

# In this exercise, you'll be working with generators to efficiently process large datasets.
# You'll implement a generator function that reads data from a file and yields processed data.

# Problem:
# You have a large file named "data.txt" that contains integer values, one per line.
# Your task is to create a generator function that reads the values from the file, processes them,
# and yields the processed values. The processing step involves multiplying each value by 2.

# Step 1: Implement the generator function
# - Create a function named `process_data` that takes a file path as a parameter.
# - Open the file and read each line using a loop.
# - For each line, convert the value to an integer, multiply it by 2, and yield the result.

# Step 2: Use the generator function
# - Create a generator object by calling the `process_data` function with the file path "data.txt".
# - Iterate over the generator object and print each processed value.

# Example usage:
# generator = process_data("data.txt")
# for value in generator:
#     print(value)

# Assume the contents of "data.txt" are:
# 1
# 2
# 3
# 4
# 5

# Expected output:
# 2
# 4
# 6
# 8
# 10

# Explanation:
# The `process_data` generator function reads each value from the file, multiplies it by 2,
# and yields the result. The generator allows you to process the data lazily, one value at a time,
# without loading the entire dataset into memory at once. This is particularly useful when dealing
# with large files or when you only need to process a subset of the data.

# Note: Make sure to create a file named "data.txt" with the example contents before running the code.
