# models/order.py

# นำเข้าตัวแปรวันเวลาปัจจุบันเพื่อใช้งานสร้างประวัติบิล
import datetime
# นำเข้าเครื่องมือ List กำหนดระเบียบอาร์เรย์ข้อมูล
from typing import List
# นำเข้าออบเจกต์อาหารสำหรับกำหนดสัดส่วนสั่งซื้อ
from models.food import Food

# คลาสรายการอาหารแต่ละจานและจำนวนจานที่สั่งในตะกร้า
class OrderItem:
    
    def __init__(self, food: Food, quantity: int):
        # ป้องกันป้อนจำนวนสินค้าเป็นศูนย์หรือติดลบ
        if quantity <= 0:
            raise ValueError("จำนวนสินค้าต้องมากกว่า 0")
        # ผูกออบเจกต์อาหารลงในตัวแปรประวัติสินค้า
        self.food = food
        # บันทึกจำนวนจานที่ต้องการสั่งซื้อ
        self.quantity = int(quantity)

    @property
    def subtotal(self) -> float:
        # คำนวณราคารวมเฉพาะเมนูนี้ (ราคาขายต่อจาน * จำนวนจาน)
        return self.food.price * self.quantity

    def to_dict(self) -> dict:
        # แปลงรายละเอียดสินค้าสั่งซื้อย่อยเป็น Dictionary
        return {
            "food_name": self.food.nameTH,
            "category": self.food.category,
            "unit_price": self.food.price,
            "quantity": self.quantity,
            "subtotal": self.subtotal
        }

# คลาสบิลสั่งซื้อและบันทึกช่องทางจ่ายเงินจำลอง
class Order:
    
    def __init__(self, order_id: str, items: List[OrderItem], payment_method: str = "Cash"):
        # เก็บรหัสสุ่มใบอ้างอิงออเดอร์
        self.order_id = order_id
        # เก็บรายการสินค้าสั่งซื้อทั้งหมดในบิล
        self.items = items
        # เก็บบันทึกประเภทช่องทางจ่ายเงิน
        self.payment_method = payment_method
        # ตั้งค่าแรกเริ่มสถานะเป็นรอจ่ายเงิน (pending)
        self.status = "pending"  
        # ดึงวันและเวลาปัจจุบันมาฟอร์แมตข้อความประวัติ
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def total_price(self) -> float:
        # วนลูปบวกผลรวมยอด subtotal สินค้าทุกชิ้นในบิล
        return sum(item.subtotal for item in self.items)

    def mark_as_paid(self):
        # เปลี่ยนสถานะเป็นโอนสำเร็จ (paid)
        self.status = "paid"
        # ไล่อัปเดตสถิติความนิยมอาหารยอดฮิตให้กับทุกรายการสั่งซื้อในบิลนี้
        for item in self.items:
            # เพิ่มคะแนนความนิยมสะสมตามจำนวนจานสินค้าสั่งซื้อ
            item.food.popularity += item.quantity

    def mark_as_cancelled(self):
        # เปลี่ยนสถานะของบิลนี้ให้กลายเป็นยกเลิกแล้ว
        self.status = "cancelled"

    def to_dict(self) -> dict:
        # แปลงข้อมูลออเดอร์และรายการสินค้าทั้งหมดเป็น Dictionary
        return {
            "order_id": self.order_id,
            "items": [item.to_dict() for item in self.items], # แปลง Dictionary ย่อยทุกรายการสินค้าในบิล
            "total_price": self.total_price,
            "status": self.status,
            "payment_method": self.payment_method,
            "created_at": self.created_at
        }
