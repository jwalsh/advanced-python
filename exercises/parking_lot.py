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
