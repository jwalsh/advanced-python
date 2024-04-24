# Metaclasses Exercise

# In this exercise, you'll be working with metaclasses to customize the behavior of class creation.
# You'll create a metaclass that logs information about the classes being created.

# Problem:
# You want to keep track of the classes being created in your program. Your task is to create a metaclass
# named 'LoggingMeta' that logs the name of each class being created and the total number of classes created.

# Step 1: Implement the LoggingMeta metaclass
# - Create a class named 'LoggingMeta' that inherits from 'type'.
# - Implement the '__new__' method to capture the class creation process.
# - Inside the '__new__' method, log the name of the class being created.
# - Keep track of the total number of classes created using a class variable.
# - Log the total number of classes created after each class creation.
# - Return the newly created class using 'super().__new__()'.

class LoggingMeta(type):
    class_count = 0

    def __new__(cls, name, bases, attrs):
        print(f"Creating class: {name}")
        new_class = super().__new__(cls, name, bases, attrs)
        LoggingMeta.class_count += 1
        print(f"Total classes created: {LoggingMeta.class_count}")
        return new_class

# Step 2: Create classes using the LoggingMeta metaclass
# - Create a few classes that use 'LoggingMeta' as their metaclass.
# - Instantiate objects from these classes.

class MyClass(metaclass=LoggingMeta):
    pass

class AnotherClass(metaclass=LoggingMeta):
    pass

obj1 = MyClass()
obj2 = AnotherClass()
obj3 = MyClass()

# Example usage:
# class MyClass(metaclass=LoggingMeta):
#     pass
# 
# class AnotherClass(metaclass=LoggingMeta):
#     pass
#
# obj1 = MyClass()
# obj2 = AnotherClass()
# obj3 = MyClass()

# Expected output:
# Creating class: MyClass
# Total classes created: 1
# Creating class: AnotherClass
# Total classes created: 2
# Creating class: MyClass
# Total classes created: 2

# Explanation:
# The 'LoggingMeta' metaclass overrides the '__new__' method to customize the class creation process.
# Inside the '__new__' method, we log the name of the class being created and keep track of the total
# number of classes created using a class variable. This allows us to monitor and log information about
# the classes being created throughout the program.

# Note: The total number of classes created is incremented only when a new unique class is created.
# Instantiating objects from existing classes does not increment the count.
