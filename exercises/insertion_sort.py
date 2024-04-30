# Insertion Sort

# Problem: Given a list of numbers, sort them in ascending order using the insertion sort algorithm.

# Imports

# Code


def insertion_sort(arr):
    """
    Sorts a list of numbers in ascending order using the insertion sort algorithm.
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            arr[j + 1] = key

    return arr


# Test the insertion_sort function
arr = [12, 11, 13, 5, 6]

# Expected output: [5, 6, 11, 12, 13]
print(insertion_sort(arr))


##


# Insertion Sort
# Implement Insertion Sort and return intermediate states.

# Insertion Sort is a simple sorting algorithm that builds the sorted list one element at a time, from left to right. It works by repeatedly taking an element from the unsorted portion and inserting it into its correct position in the sorted portion of the list.

# Objective:

# Given a list of key-value pairs, sort the list by key using Insertion Sort. Return a list of lists showing the state of the array after each insertion. If two key-value pairs have the same key, maintain their relative order in the sorted list.

# Input:

# pairs - a list of key-value pairs, where each key-value has an integer key and a string value. (0 <= pairs.length <= 100).
# Example 1:

# Input:
# pairs = [(5, "apple"), (2, "banana"), (9, "cherry")]


def insertion_sort(pairs):
    """
    Sorts a list of key-value pairs by key using the Insertion Sort algorithm.
    Returns a list of lists showing the state of the array after each insertion.
    """
    states = [pairs.copy()]
    for i in range(1, len(pairs)):
        key = pairs[i]
        j = i - 1
        while j >= 0 and key[0] < pairs[j][0]:
            pairs[j + 1] = pairs[j]
            j -= 1
        pairs[j + 1] = key
        states.append(pairs.copy())
    return states


# Output:
# [[(5, "apple"), (2, "banana"), (9, "cherry")],
#  [(2, "banana"), (5, "apple"), (9, "cherry")],
#  [(2, "banana"), (5, "apple"), (9, "cherry")]]
# Notice that the output shows the state of the array after each insertion. The last state is the final sorted array. There should be pairs.length states in total.

# Example 2:

# Input:
# pairs = [(3, "cat"), (3, "bird"), (2, "dog")]

# Output:
# [[(3, "cat"), (3, "bird"), (2, "dog")],
#  [(3, "cat"), (3, "bird"), (2, "dog")],
#  [(2, "dog"), (3, "cat"), (3, "bird")]]
# In this example, you can observe that the pairs with key=3 ("cat" and "bird") maintain their relative order, illustrating the stability of the Insertion Sort algorithm.

# Accepted: 3678  |  Submitted: 23663  |  Acceptance Rate: 16%
# 12345678
# # Definition for a pair.
# # class Pair:
# #     def __init__(self, key: int, value: str):
# #         self.key = key
# #         self.value = value
# class Solution:
#     def insertionSort(self, pairs: List[Pair]) -> List[List[Pair]]:


# # Definition for a pair.
# # class Pair:
# #     def __init__(self, key: int, value: str):
# #         self.key = key
# #         self.value = value
# class Solution:
#     def insertionSort(self, pairs: List[Pair]) -> List[List[Pair]]:
#         states = [pairs.copy()]
#         for i in range(1, len(pairs)):
#             key = pairs[i]
#             j = i - 1
#             while j >= 0 and key.key < pairs[j].key:
#                 pairs[j + 1] = pairs[j]
#                 j -= 1
#             pairs[j + 1] = key
#             states.append(pairs.copy())
#         return states
