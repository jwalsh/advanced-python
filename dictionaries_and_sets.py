# Dictionaries and Sets Exercise

# TODO: Complete the exercise
nums = [100,4,200,1,3,2]
nums_set = set(nums)
freq = {}
for num in nums:
    if num in freq:
        freq[num] += 1
    else:
        freq[num] = 1

    
