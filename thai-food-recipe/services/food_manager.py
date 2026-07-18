# services/food_manager.py

# นำเข้าตัวควบคุมชนิดตัวแปรที่ใช้สืบค้น
from typing import List, Optional
# นำเข้าคลาสหลักของอาหาร
from models.food import Food
# นำเข้าเครื่องมือดึงคลังอาหาร 100 เมนู
from models.food_list import get_100_thai_foods

# คลาสบริการคัดแยก หมวดหมู่ ค้นหา และสถิติอาหาร (Singleton Pattern)
class FoodManager:
    # เก็บรักษาสถานะออบเจกต์เดี่ยวแชร์ร่วมกัน
    _instance = None

    def __new__(cls, *args, **kwargs):
        # บังคับสร้างอินสแตนซ์ของคลาสเพียงตัวเดียว (Singleton Pattern)
        if not cls._instance:
            # สร้างตัวแปรออบเจกต์ชิ้นเดี่ยวเก็บใน _instance
            cls._instance = super(FoodManager, cls).__new__(cls, *args, **kwargs)
            # ปรับเปลี่ยนสถานะการตั้งค่าเริ่มแรกเป็น False
            cls._instance._initialized = False
        # คืนค่าออบเจกต์ตัวจัดการข้อมูลอาหารเดี่ยว
        return cls._instance

    def __init__(self):
        # เช็คหากเคยตั้งค่าคลังอาหารไปแล้วให้ข้ามทันที
        if self._initialized:
            return
        # โหลดฐานข้อมูลอาหาร 100 จานมาเก็บไว้บนหน่วยความจำ RAM Cache
        self.foods: List[Food] = get_100_thai_foods()
        # เปลี่ยนสถานะเตรียมพร้อมข้อมูลเริ่มต้นเป็น True
        self._initialized = True

    def get_all_foods(self) -> List[Food]:
        # ดึงลิสต์ของเมนูอาหารทั้งหมด
        return self.foods

    def get_foods_by_category(self, category: str) -> List[Food]:
        # กรองรายการอาหารเฉพาะหมวดหมู่ประเภทที่กำหนดตรงกัน
        return [f for f in self.foods if f.category == category]

    def search_foods(self, query: str) -> List[Food]:
        # ค้นหาเมนูอาหารอัจฉริยะ (ค้นเจอได้ทั้งจากชื่อเมนู และตรวจจากชื่อวัตถุดิบข้างในสูตร)
        if not query:
            # หากไม่มีคำค้นหาให้ส่งคืนอาหารทั้งหมด 100 เมนูโดยไม่ต้องกรอง
            return self.foods
        
        # ตัดช่องว่างหัวท้ายข้อความและแปลงตัวอักษรเป็นพิมพ์เล็ก
        query = query.lower().strip()
        # เตรียมลิสต์เปล่าเก็บประวัติอาหารที่ค้นเจอ
        results = []
        # วนลูปสืบค้นเมนูอาหารทีละรายการ
        for food in self.foods:
            # 1. ตรวจสอบเงื่อนไขชื่ออาหารตรงตามคำสืบค้นหรือไม่
            if query in food.nameTH.lower():
                # เพิ่มเข้าลิสต์ผลลัพธ์
                results.append(food)
                # ข้ามไปตรวจจานถัดไปในลิสต์ทันทีเพื่อความเร็ว
                continue
            
            # 2. ตรวจสอบสูตรผสมวัตถุดิบข้างในสูตรปรุงอาหารจานนั้นๆ
            for recipe_item in food.recipeList:
                # เช็คคำสืบค้นตรงกับชื่อวัตถุดิบชิ้นใดชิ้นหนึ่งในสูตรปรุง
                if query in recipe_item.recipeName.lower():
                    # เพิ่มเข้าลิสต์ผลลัพธ์การค้นหา
                    results.append(food)
                    # หยุดลูปการตรวจสอบส่วนผสมอื่นในจานนี้ เพื่อไม่ให้เกิดจานเดิมซ้ำ
                    break
        # คืนลิสต์ผลการค้นหาทั้งหมดกลับไป
        return results

    def get_food_by_name(self, name: str) -> Optional[Food]:
        # สืบหาข้อมูลรายละเอียดอาหารโดยอ้างอิงจากสะกดชื่อจานตรงกัน
        for food in self.foods:
            if food.nameTH == name:
                # คืนออบเจกต์อาหารจานนั้น
                return food
        # คืนค่าว่างกรณีหาอาหารจานดังกล่าวไม่พบ
        return None

    def get_popular_foods(self, limit: int = 6) -> List[Food]:
        # จัดเรียงเมนูที่ขายดีสูงสุดโดยเรียงลำดับยอดความนิยมมากสุดไปน้อยสุด (ใส่เครื่องหมายลบ -)
        sorted_foods = sorted(self.foods, key=lambda f: (-f.popularity, f.nameTH))
        # ดึงลิสต์และจำกัดจำนวนข้อมูลยอดฮิตตามพารามิเตอร์ limit
        return sorted_foods[:limit]
