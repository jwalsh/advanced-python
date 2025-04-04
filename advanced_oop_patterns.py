# Advanced OOP Patterns Exercise

# In this exercise, you'll be implementing three common design patterns in Python:
# Singleton, Factory, and Observer. Each pattern will be implemented as a separate class.

# Problem:
# You're developing a system that requires the following functionality:
# 1. A logger class that follows the Singleton pattern to ensure only one instance of the logger is created.
# 2. A shape factory class that creates different shapes based on a given type.
# 3. An observable class that notifies its observers whenever its state changes.


# Step 1: Implement the Singleton pattern
# - Create a class named 'Logger' that follows the Singleton pattern.
# - Ensure that only one instance of the Logger class can be created.
# - Implement a method named 'log' that prints a message to the console.
class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def log(self, message):
        print(message)


# Step 2: Implement the Factory pattern
# - Create an abstract base class named 'Shape' with an abstract method 'draw'.
# - Create concrete classes 'Circle' and 'Square' that inherit from 'Shape' and implement the 'draw' method.
# - Create a factory class named 'ShapeFactory' that creates instances of 'Circle' or 'Square' based on a given type.

# Step 3: Implement the Observer pattern
# - Create a class named 'Subject' that represents an observable object.
# - Implement methods 'attach', 'detach', and 'notify' to manage observers and notify them of state changes.
# - Create a class named 'Observer' that represents an observer object.
# - Implement a method named 'update' that is called when the subject's state changes.

# Example usage:
# # Singleton pattern
# logger1 = Logger()
# logger2 = Logger()
# logger1.log("This is a log message")
# logger2.log("Another log message")
#
# # Factory pattern
# shape_factory = ShapeFactory()
# circle = shape_factory.create_shape("circle")
# square = shape_factory.create_shape("square")
# circle.draw()
# square.draw()
#
# # Observer pattern
# subject = Subject()
# observer1 = Observer("Observer 1")
# observer2 = Observer("Observer 2")
# subject.attach(observer1)
# subject.attach(observer2)
# subject.state = "New state"
# subject.notify()

# Expected output:
# This is a log message
# Another log message
# Drawing a circle
# Drawing a square
# Observer 1 received update: New state
# Observer 2 received update: New state

# Explanation:
# The Singleton pattern ensures that only one instance of the Logger class is created, even if multiple instances are requested.
# The Factory pattern allows the creation of objects based on a given type, without exposing the instantiation logic to the client.
# The Observer pattern defines a one-to-many dependency between objects, so that when one object changes state, all its dependents are notified and updated automatically.

# Note: You can expand upon the example usage and add more test cases to verify the behavior of each pattern.
