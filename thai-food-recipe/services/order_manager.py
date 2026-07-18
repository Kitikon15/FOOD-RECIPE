# services/order_manager.py

# นำเข้าตัวดึงรหัสจำลองอ้างอิงธุรกรรม
import uuid
# นำเข้าเครื่องมือกำหนดระเบียบตัวแปร
from typing import List, Optional
# นำเข้าโมเดลใบสั่งซื้อและประวัติตะกร้า
from models.order import Order, OrderItem
# นำเข้าตัวจัดการอาหารเพื่อเทียบราคา
from services.food_manager import FoodManager

# คลาสบริการบันทึกประวัติ ประมวลยอดขาย และยืนยันโอนเงิน (Singleton Pattern)
class OrderManager:
    # เก็บรักษาสถานะออบเจกต์เดี่ยวแชร์ประวัติ
    _instance = None

    def __new__(cls, *args, **kwargs):
        # บังคับสร้างอินสแตนซ์ของคลาสตัวจัดการเพียงชิ้นเดียว (Singleton Pattern)
        if not cls._instance:
            # สร้างตัวแปรออบเจกต์ตัวตนเดี่ยวเก็บใน _instance
            cls._instance = super(OrderManager, cls).__new__(cls, *args, **kwargs)
            # ปรับเปลี่ยนสถานะแรกเริ่มข้อมูลเป็น False
            cls._instance._initialized = False
        # คืนออบเจกต์ตัวจัดการบิลใบสั่งซื้อ
        return cls._instance

    def __init__(self):
        # ข้ามทันทีถ้าเคยประกาศประวัติตั้งต้นระบบไปแล้ว
        if self._initialized:
            return
        # ลิสต์เก็บประวัติคำสั่งซื้อทั้งหมดที่ดำเนินการสำเร็จ
        self.orders: List[Order] = []
        # ดึงออบเจกต์การจัดการข้อมูลอาหารมาผูกใช้งาน
        self.food_manager = FoodManager()
        # เรียกเติมข้อมูลบิลและยอดขายสะสมสะใจจำลองเพื่อความสวยงามในระบบ
        self._seed_mock_orders()
        # เปลี่ยนสถานะเตรียมพร้อมระบบเริ่มต้นเป็น True
        self._initialized = True

    def _seed_mock_orders(self):
        # จำลองการโอนสั่งซื้อสะสมเพื่อช่วยตกแต่งประวัติการสั่งซื้อเริ่มต้น
        # 1. จำลองสร้างใบสั่งซื้อใบที่ 1 (จ่ายเงินผ่าน PromptPay เรียบร้อยแล้ว)
        grapow = self.food_manager.get_food_by_name("ข้าวกะเพราหมูกรอบ")
        tomyum = self.food_manager.get_food_by_name("ต้มยำกุ้ง")
        if grapow and tomyum:
            item1 = OrderItem(grapow, 2)
            item2 = OrderItem(tomyum, 1)
            order1 = Order(order_id="ORD-9021", items=[item1, item2], payment_method="PromptPay")
            order1.mark_as_paid() # เปลี่ยนสถานะเงินเป็นชำระสำเร็จ และบวกยอดฮิตเมนูจานสั่งซื้อ
            self.orders.append(order1)

        # 2. จำลองสร้างใบสั่งซื้อใบที่ 2 (จ่ายเงินผ่านบัตรเครดิตเรียบร้อยแล้ว)
        padthai = self.food_manager.get_food_by_name("ผัดไทยกุ้งสด")
        if padthai:
            item1 = OrderItem(padthai, 1)
            order2 = Order(order_id="ORD-7832", items=[item1], payment_method="Credit Card")
            order2.mark_as_paid()
            self.orders.append(order2)

        # 3. จำลองสร้างใบสั่งซื้อใบที่ 3 (รอชำระเงินที่แคชเชียร์)
        kana = self.food_manager.get_food_by_name("ข้าวผัดคะน้าหมูกรอบ")
        if kana:
            item1 = OrderItem(kana, 1)
            order3 = Order(order_id="ORD-5231", items=[item1], payment_method="Cash")
            self.orders.append(order3)

    def create_order(self, items_data: List[dict], payment_method: str = "Cash") -> Order:
        # ดำเนินการสร้างใบคำสั่งซื้อใบใหม่จากสินค้าที่ลูกค้ากดสั่งซื้อ
        order_items = []
        # วนลูปตรวจสอบข้อมูลวัตถุดิบและสร้างรายการย่อยสินค้าในตะกร้า
        for item in items_data:
            food_name = item.get("food_name")
            quantity = item.get("quantity", 1)
            
            # เรียกข้อมูลราคาขายล่าสุดของเมนูนั้นๆ
            food = self.food_manager.get_food_by_name(food_name)
            # กรณีตรวจไม่พบสะกดชื่อสินค้าในระบบ 100 เมนู
            if not food:
                # แจ้งระบุไม่มีเมนูอาหารและหยุดการทำงานสั่งซื้อ
                raise ValueError(f"ไม่พบเมนูอาหาร '{food_name}'")
            
            # เพิ่มรายการออบเจกต์ OrderItem
            order_items.append(OrderItem(food, quantity))

        # ป้องกันกดชำระเงินโดยไม่มีรายการในตะกร้าสินค้า
        if not order_items:
            raise ValueError("คำสั่งซื้อต้องมีรายการอย่างน้อย 1 รายการ")

        # สุ่มหมายเลขอ้างอิงออเดอร์ในรูปแบบ ORD-xxxx
        import random
        order_id = f"ORD-{random.randint(1000, 9999)}"
        
        # ดำเนินการสร้างออบเจกต์คำสั่งซื้อใหม่ (Order Object)
        new_order = Order(order_id=order_id, items=order_items, payment_method=payment_method)
        # เก็บใบสั่งซื้อใบใหม่เข้าคลังประวัติ orders ของระบบหลังบ้าน
        self.orders.append(new_order)
        # ส่งค่าออบเจกต์ออเดอร์ใหม่เพื่อนำไปใช้แสดงรายละเอียดบนหน้าบิล
        return new_order

    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        # ค้นหาใบสั่งซื้อตามหมายเลขออเดอร์ที่ระบุในคลัง
        for order in self.orders:
            if order.order_id == order_id:
                # คืนออบเจกต์บิลสั่งซื้อที่ค้นพบ
                return order
        # คืนค่าว่างถ้าไม่พบบิล
        return None

    def pay_order(self, order_id: str) -> Optional[Order]:
        # ดำเนินธุรกรรมยืนยันชำระเงินออเดอร์ในระบบหลังบ้าน
        order = self.get_order_by_id(order_id)
        # ตรวจเช็คว่าตรวจพบใบสั่งซื้อและบิลดังกล่าวอยู่ในสถานะรอชำระเงิน (pending)
        if order and order.status == "pending":
            # ปรับเปลี่ยนสถานะบิลเป็นชำระเรียบร้อย และสะสมคะแนนจานอาหารขายดี
            order.mark_as_paid()
            # ส่งคืนใบสั่งซื้อที่ทำรายการจ่ายเงินเสร็จสิ้น
            return order
        # คืนออบเจกต์เดิม
        return order

    def get_order_history(self) -> List[Order]:
        # ดึงลิสต์บิลใบประวัติคำสั่งซื้อทั้งหมดเรียงลำดับเวลาใหม่สุดไปหาเก่าสุด
        return sorted(self.orders, key=lambda o: o.created_at, reverse=True)
