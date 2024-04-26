#!/bin/sh

# Create the exercises directory
mkdir -p exercises

# Exercise 1: System Design
cat > exercises/parking_lot.py <<'EOL'
# Exercise: Parking Lot System Design
# Design a parking lot system that can handle different types of vehicles and parking spots.

from abc import ABC, abstractmethod

class Vehicle(ABC):
    # Your code here
    pass

class Car(Vehicle):
    # Your code here
    pass

class Motorcycle(Vehicle):
    # Your code here
    pass

class ParkingSpot(ABC):
    # Your code here
    pass

class CarSpot(ParkingSpot):
    # Your code here
    pass

class MotorcycleSpot(ParkingSpot):
    # Your code here
    pass

class ParkingLot:
    # Your code here
    pass

if __name__ == "__main__":
    parking_lot = ParkingLot(2, 1)
    car1 = Car("ABC123")
    car2 = Car("XYZ789")
    motorcycle = Motorcycle("M1234")

    parking_lot.park_vehicle(car1)
    parking_lot.park_vehicle(car2)
    parking_lot.park_vehicle(motorcycle)

    print(parking_lot.unpark_vehicle(car1))
    print(parking_lot.unpark_vehicle(motorcycle))
EOL

cat > exercises/test_parking_lot.py <<'EOL'
import unittest
from parking_lot import ParkingLot, Car, Motorcycle

class TestParkingLot(unittest.TestCase):
    def test_parking_lot(self):
        parking_lot = ParkingLot(2, 1)
        car1 = Car("ABC123")
        car2 = Car("XYZ789")
        motorcycle = Motorcycle("M1234")

        self.assertTrue(parking_lot.park_vehicle(car1))
        self.assertTrue(parking_lot.park_vehicle(car2))
        self.assertTrue(parking_lot.park_vehicle(motorcycle))

        self.assertEqual(parking_lot.unpark_vehicle(car1), "ABC123")
        self.assertEqual(parking_lot.unpark_vehicle(motorcycle), "M1234")

if __name__ == "__main__":
    unittest.main()
EOL

# Exercise 2: Architectural Patterns
cat > exercises/event_driven_architecture.py <<'EOL'
# Exercise: Event-Driven Architecture
# Implement an event-driven architecture for a simple e-commerce application.

class EventBus:
    # Your code here
    pass

class Order:
    # Your code here
    pass

class InventoryService:
    # Your code here
    pass

class PaymentService:
    # Your code here
    pass

class ShippingService:
    # Your code here
    pass

if __name__ == "__main__":
    event_bus = EventBus()
    inventory_service = InventoryService(event_bus)
    payment_service = PaymentService(event_bus)
    shipping_service = ShippingService(event_bus)

    order = Order(1, "Product A", 10.0)
    event_bus.publish("order_placed", order)
EOL

cat > exercises/test_event_driven_architecture.py <<'EOL'
import unittest
from unittest.mock import MagicMock
from event_driven_architecture import EventBus, Order, InventoryService, PaymentService, ShippingService

class TestEventDrivenArchitecture(unittest.TestCase):
    def test_event_driven_architecture(self):
        event_bus = EventBus()
        inventory_service = InventoryService(event_bus)
        payment_service = PaymentService(event_bus)
        shipping_service = ShippingService(event_bus)

        inventory_service.update_inventory = MagicMock()
        payment_service.process_payment = MagicMock()
        shipping_service.ship_order = MagicMock()

        order = Order(1, "Product A", 10.0)
        event_bus.publish("order_placed", order)

        inventory_service.update_inventory.assert_called_once_with(order)
        payment_service.process_payment.assert_called_once_with(order)
        shipping_service.ship_order.assert_called_once_with(order)

if __name__ == "__main__":
    unittest.main()
EOL

# Exercise 3: Scalability and Performance
cat > exercises/rate_limiter.py <<'EOL'
# Exercise: Rate Limiter
# Implement a rate limiter to control the rate of requests to an API.

import time

class RateLimiter:
    def __init__(self, limit, window):
        # Your code here
        pass

    def allow_request(self):
        # Your code here
        pass

if __name__ == "__main__":
    rate_limiter = RateLimiter(5, 10)  # 5 requests per 10 seconds

    for _ in range(10):
        if rate_limiter.allow_request():
            print("Request allowed")
        else:
            print("Request blocked")
        time.sleep(1)
EOL

cat > exercises/test_rate_limiter.py <<'EOL'
import unittest
from rate_limiter import RateLimiter

class TestRateLimiter(unittest.TestCase):
    def test_rate_limiter(self):
        rate_limiter = RateLimiter(5, 10)

        # Allow 5 requests
        for _ in range(5):
            self.assertTrue(rate_limiter.allow_request())

        # Block the next request
        self.assertFalse(rate_limiter.allow_request())

if __name__ == "__main__":
    unittest.main()
EOL

# More exercises...

echo "Exercises and test files created successfully."
