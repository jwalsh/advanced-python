#!/usr/bin/env python3
"""
Abstract Base Classes in Python
==============================

This module demonstrates the use of Abstract Base Classes (ABCs) in Python
to define interfaces, enforce implementation of required methods, and
create more robust and well-structured object hierarchies.

Key concepts covered:
- Basic ABC definition with @abstractmethod
- Interface enforcement
- Abstract properties
- ABC registration
- Protocol classes (Python 3.8+)
- Real-world use cases

ABCs help address the limitations of duck typing when more
explicit interfaces are needed.
"""

import abc
from abc import ABC, abstractmethod
from collections.abc import Sequence, Mapping
import sys
from typing import Protocol, runtime_checkable

# Basic ABC Example
class Shape(ABC):
    """Abstract base class representing a geometric shape."""
    
    @abstractmethod
    def area(self):
        """Calculate the area of the shape."""
        pass
    
    @abstractmethod
    def perimeter(self):
        """Calculate the perimeter of the shape."""
        pass
    
    def describe(self):
        """Non-abstract method that subclasses inherit without overriding."""
        return f"This shape has area {self.area()} and perimeter {self.perimeter()}"


# Concrete implementation of Shape
class Rectangle(Shape):
    """A rectangle implementation of the Shape ABC."""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)


class Circle(Shape):
    """A circle implementation of the Shape ABC."""
    
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        import math
        return 2 * math.pi * self.radius


# Abstract Properties Example
class DataSource(ABC):
    """Abstract base class for data sources with required properties."""
    
    @property
    @abstractmethod
    def name(self):
        """The name of the data source."""
        pass
    
    @property
    @abstractmethod
    def connection_string(self):
        """The connection string for the data source."""
        pass
    
    @abstractmethod
    def connect(self):
        """Connect to the data source."""
        pass
    
    @abstractmethod
    def fetch_data(self, query):
        """Fetch data from the data source."""
        pass


class DatabaseSource(DataSource):
    """A database implementation of DataSource."""
    
    def __init__(self, db_name, host="localhost", port=5432):
        self._db_name = db_name
        self._host = host
        self._port = port
    
    @property
    def name(self):
        return f"Database: {self._db_name}"
    
    @property
    def connection_string(self):
        return f"postgresql://{self._host}:{self._port}/{self._db_name}"
    
    def connect(self):
        print(f"Connecting to {self.connection_string}")
        # In real code: return psycopg2.connect(self.connection_string)
    
    def fetch_data(self, query):
        print(f"Executing query on {self.name}: {query}")
        # In real code: return conn.execute(query).fetchall()


# Advanced: Abstract Base Class Registration
class JSONSerializable(ABC):
    """Abstract base class for objects that can be serialized to JSON."""
    
    @abstractmethod
    def to_json(self):
        """Convert the object to a JSON-compatible dictionary."""
        pass
    
    @classmethod
    def __subclasshook__(cls, subclass):
        """Special method to determine if a class is a subclass without explicit inheritance."""
        if cls is JSONSerializable:
            if any("to_json" in B.__dict__ for B in subclass.__mro__):
                return True
        return NotImplemented


# This class doesn't inherit from JSONSerializable but can be registered with it
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def to_json(self):
        return {"name": self.name, "email": self.email}


# Register User as a virtual subclass of JSONSerializable
JSONSerializable.register(User)


# Python 3.8+ Protocol Example (Static Duck Typing)
@runtime_checkable
class Drawable(Protocol):
    """A protocol defining objects that can be drawn."""
    
    def draw(self) -> None:
        """Draw the object."""
        ...


class Canvas:
    """A canvas that can draw any Drawable object."""
    
    def __init__(self):
        self.elements = []
    
    def add_element(self, element):
        """Add an element to the canvas."""
        if isinstance(element, Drawable):
            self.elements.append(element)
        else:
            raise TypeError("Element must be Drawable")
    
    def draw_all(self):
        """Draw all elements on the canvas."""
        for element in self.elements:
            element.draw()


# This class satisfies the Drawable protocol without explicit inheritance
class Button:
    """A button that can be drawn."""
    
    def __init__(self, label):
        self.label = label
    
    def draw(self):
        print(f"Drawing button: {self.label}")


# Real-world Example: Custom Container with ABC
class SortedItems(Sequence):
    """A sequence that keeps items in sorted order."""
    
    def __init__(self, items=None):
        self._items = sorted(items) if items else []
    
    def __getitem__(self, index):
        return self._items[index]
    
    def __len__(self):
        return len(self._items)
    
    def add(self, item):
        """Add an item to the collection, maintaining sorted order."""
        self._items.append(item)
        self._items.sort()


# Interactive Exercises
def exercises():
    """Exercises for abstract base classes"""
    print("\nExercises:")
    
    # Exercise 1: Create a FileHandler ABC with concrete implementations
    print("Exercise 1: Create a FileHandler ABC with methods read() and write()")
    # Your solution here
    
    # Exercise 2: Implement a Validator protocol for data validation
    print("Exercise 2: Implement a Validator protocol")
    # Your solution here
    
    # Exercise 3: Create a custom ABC for caching mechanisms
    print("Exercise 3: Create a Cacheable ABC")
    # Your solution here


# Main function
if __name__ == "__main__":
    print("Abstract Base Classes in Python\n")
    
    # Demonstrate basic ABC
    rectangle = Rectangle(5, 10)
    circle = Circle(7)
    
    print("Basic ABC Example:")
    print(f"Rectangle area: {rectangle.area()}, perimeter: {rectangle.perimeter()}")
    print(f"Circle area: {circle.area():.2f}, perimeter: {circle.perimeter():.2f}")
    print(f"Rectangle description: {rectangle.describe()}")
    print()
    
    # Demonstrate abstract properties
    db = DatabaseSource("customers_db")
    print("Abstract Properties Example:")
    print(f"Data source: {db.name}")
    print(f"Connection: {db.connection_string}")
    db.connect()
    db.fetch_data("SELECT * FROM customers")
    print()
    
    # Demonstrate ABC registration
    user = User("Alice", "alice@example.com")
    print("ABC Registration Example:")
    print(f"Is User a subclass of JSONSerializable? {issubclass(User, JSONSerializable)}")
    print(f"Is user an instance of JSONSerializable? {isinstance(user, JSONSerializable)}")
    print(f"User as JSON: {user.to_json()}")
    print()
    
    # Demonstrate Protocol
    if sys.version_info >= (3, 8):
        print("Protocol Example (Python 3.8+):")
        canvas = Canvas()
        button = Button("Click me")
        try:
            canvas.add_element(button)
            print("Button added to canvas")
            canvas.draw_all()
        except TypeError as e:
            print(f"Error: {e}")
        
        # This would fail:
        # canvas.add_element("not drawable")
        print()
    
    # Demonstrate custom container with ABC
    print("Custom Container Example:")
    sorted_items = SortedItems([3, 1, 5, 2, 4])
    print(f"Items: {list(sorted_items)}")
    sorted_items.add(0)
    print(f"After adding 0: {list(sorted_items)}")
    print(f"Item at index 2: {sorted_items[2]}")
    print(f"Length: {len(sorted_items)}")
    print()
    
    # Run exercises
    exercises()