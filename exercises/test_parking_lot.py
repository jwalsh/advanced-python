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
