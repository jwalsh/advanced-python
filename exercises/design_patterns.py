# Exercise: Design Patterns
# Implement a singleton pattern and a factory pattern in Python.


# Singleton Pattern
class Singleton:
    # Your code here
    pass


# Factory Pattern
class ShapeFactory:
    # Your code here
    pass


if __name__ == "__main__":
    # Test Singleton
    s1 = Singleton()
    s2 = Singleton()
    print(s1 == s2)  # Output: True

    # Test Factory
    factory = ShapeFactory()
    circle = factory.create_shape("circle")
    square = factory.create_shape("square")
    print(circle.draw())  # Output: Drawing a circle
    print(square.draw())  # Output: Drawing a square
