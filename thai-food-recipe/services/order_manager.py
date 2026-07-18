import uuid
from typing import List, Optional
from models.order import Order, OrderItem
from services.food_manager import FoodManager

class OrderManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OrderManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.orders: List[Order] = []
        self.food_manager = FoodManager()
        self._seed_mock_orders()
        self._initialized = True

    def _seed_mock_orders(self):
        # Seed 3 mock orders to populate history and make the dashboard look alive
        # Order 1 (Paid)
        grapow = self.food_manager.get_food_by_name("ข้าวกะเพราหมูกรอบ")
        tomyum = self.food_manager.get_food_by_name("ต้มยำกุ้ง")
        if grapow and tomyum:
            item1 = OrderItem(grapow, 2)
            item2 = OrderItem(tomyum, 1)
            order1 = Order(order_id="ORD-9021", items=[item1, item2], payment_method="PromptPay")
            order1.mark_as_paid()
            self.orders.append(order1)

        # Order 2 (Paid)
        padthai = self.food_manager.get_food_by_name("ผัดไทยกุ้งสด")
        if padthai:
            item1 = OrderItem(padthai, 1)
            order2 = Order(order_id="ORD-7832", items=[item1], payment_method="Credit Card")
            order2.mark_as_paid()
            self.orders.append(order2)

        # Order 3 (Pending)
        kana = self.food_manager.get_food_by_name("ข้าวผัดคะน้าหมูกรอบ")
        if kana:
            item1 = OrderItem(kana, 1)
            order3 = Order(order_id="ORD-5231", items=[item1], payment_method="Cash")
            self.orders.append(order3)

    def create_order(self, items_data: List[dict], payment_method: str = "Cash") -> Order:
        """
        items_data format: [{'food_name': '...', 'quantity': 2}, ...]
        """
        order_items = []
        for item in items_data:
            food_name = item.get("food_name")
            quantity = item.get("quantity", 1)
            
            food = self.food_manager.get_food_by_name(food_name)
            if not food:
                raise ValueError(f"ไม่พบเมนูอาหาร '{food_name}'")
            
            order_items.append(OrderItem(food, quantity))

        if not order_items:
            raise ValueError("คำสั่งซื้อต้องมีรายการอย่างน้อย 1 รายการ")

        # Generate custom human-friendly order ID
        import random
        order_id = f"ORD-{random.randint(1000, 9999)}"
        
        new_order = Order(order_id=order_id, items=order_items, payment_method=payment_method)
        self.orders.append(new_order)
        return new_order

    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None

    def pay_order(self, order_id: str) -> Optional[Order]:
        order = self.get_order_by_id(order_id)
        if order and order.status == "pending":
            order.mark_as_paid()
            return order
        return order

    def get_order_history(self) -> List[Order]:
        # Return orders sorted by creation time (newest first)
        return sorted(self.orders, key=lambda o: o.created_at, reverse=True)
