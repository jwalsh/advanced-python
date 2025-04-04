import unittest
from unittest.mock import MagicMock

from event_driven_architecture import (
    EventBus,
    InventoryService,
    Order,
    PaymentService,
    ShippingService,
)


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
