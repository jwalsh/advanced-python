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
