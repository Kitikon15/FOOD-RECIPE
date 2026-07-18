import datetime
from typing import List
from models.food import Food

class OrderItem:
    def __init__(self, food: Food, quantity: int):
        if quantity <= 0:
            raise ValueError("จำนวนสินค้าต้องมากกว่า 0")
        self.food = food
        self.quantity = int(quantity)

    @property
    def subtotal(self) -> float:
        return self.food.price * self.quantity

    def to_dict(self) -> dict:
        return {
            "food_name": self.food.nameTH,
            "category": self.food.category,
            "unit_price": self.food.price,
            "quantity": self.quantity,
            "subtotal": self.subtotal
        }

class Order:
    def __init__(self, order_id: str, items: List[OrderItem], payment_method: str = "Cash"):
        self.order_id = order_id
        self.items = items
        self.payment_method = payment_method
        self.status = "pending"  # pending, paid, cancelled
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def total_price(self) -> float:
        return sum(item.subtotal for item in self.items)

    def mark_as_paid(self):
        self.status = "paid"
        # Increment popularity for all ordered items
        for item in self.items:
            item.food.popularity += item.quantity

    def mark_as_cancelled(self):
        self.status = "cancelled"

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "items": [item.to_dict() for item in self.items],
            "total_price": self.total_price,
            "status": self.status,
            "payment_method": self.payment_method,
            "created_at": self.created_at
        }
