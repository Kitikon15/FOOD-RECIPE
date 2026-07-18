# models/food.py

# นำเข้าคลาสหมวดหมู่เพื่อใช้คัดกรองข้อมูล
from models.category import Category
# นำเข้าคลาสสัดส่วนสูตรอาหารเพื่อนำมาจัดลิสต์สูตร
from models.recipe import Recipe

# คลาสเมนูอาหาร (จัดเก็บชื่อ ประเภท ราคา คะแนน และวัตถุดิบปรุง)
class Food:
    
    def __init__(self, nameTh: str, category: str, price: float = 50.0):
        # ตรวจเช็คว่าหมวดหมู่ถูกต้องตามที่ระบบระบุไว้หรือไม่
        if not Category.is_valid(category):
            # โยนข้อผิดพลาดหากหมวดหมู่ไม่สอดคล้องตามระบบ
            raise ValueError(f"ประเภทอาหาร '{category}' ไม่ถูกต้องตามระบบ")
        
        # บันทึกข้อมูลชื่อเมนู (ภาษาไทย)
        self.nameTH = nameTh
        # ค่าบันทึกชื่อซ้ำเพื่อเพิ่มความหยืดหยุ่นการสืบค้นข้อมูล
        self.nameTh = nameTh  
        # บันทึกชื่อหมวดหมู่อาหารที่ผ่านเกณฑ์แล้ว
        self.category = category
        # ตั้งค่าลิสต์ว่างรอรับสัดส่วนสูตรวัตถุดิบปรุง
        self.recipeList = []
        # บันทึกราคาขายเฉลี่ยทศนิยม
        self.price = float(price)
        # ตั้งค่าเริ่มแรกยอดขายสะสมเป็นศูนย์
        self.popularity = 0
        
    def add_recipe(self, recipe: Recipe):
        # ตรวจสอบว่าเป็นออบเจกต์คลาส Recipe จริงก่อนบันทึก
        if isinstance(recipe, Recipe):
            # แนบตัวแปรสูตรเข้าลิสต์สะสมวัตถุดิบของอาหารจานนี้
            self.recipeList.append(recipe)
        else:
            # แจ้งข้อผิดพลาดหากนำตัวแปรชนิดอื่นที่ไม่ใช่สูตรอาหารมาแนบ
            raise TypeError("ต้องเป็นออบเจกต์ประเภท Recipe เท่านั้น")

    def display(self):
        # แสดงผลโครงสร้างเมนูและวัตถุดิบออกทางหน้าจอ Console
        print(f"============= {self.nameTH} =============")
        print(f"เมนู: {self.nameTH}")
        print(f"หมวดหมู่: {self.category}")
        print(f"ราคา: {self.price} บาท")
        print(f"ยอดสั่งซื้อ: {self.popularity} ครั้ง")
        print(f"============= {self.nameTH} =============")
        print("วัตถุดิบที่ใช้:")
        # เช็คหากไม่มีประวัติวัตถุดิบในจานนี้เลย
        if not self.recipeList:
            print(" -ไม่มีวัตถุดิบที่ใช้")
        # ลูปพิมพ์วัตถุดิบ ลำดับ สัดส่วน และหน่วยวัด
        for idx, item in enumerate(self.recipeList, start=1):
            print(f"  {idx}. {item.recipeName:<22} {item.quantity:>6} {item.unitName}")
        print(f"============= {self.nameTH} =============")

    def to_dict(self) -> dict:
        # จัดแปลงข้อมูลออบเจกต์อาหารให้อยู่ในโครงสร้าง Dictionary
        return {
            "nameTh": self.nameTH,
            "category": self.category,
            "price": self.price,
            "popularity": self.popularity,
            # วนลูปแปลงออบเจกต์สัดส่วนวัตถุดิบด้านในให้เป็น Dictionary ย่อย
            "recipeList": [item.to_dict() for item in self.recipeList]
        }