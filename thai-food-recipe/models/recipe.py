# models/recipe.py

# นำเข้าคลาสวัตถุดิบเพื่อมาประกอบสัดส่วน
from models.ingredient import Ingredient

# คลาสสัดส่วนวัตถุดิบ (ชนิดวัตถุดิบ + ปริมาณ + หน่วยวัด)
class Recipe:
    
    def __init__(self, ingredient: Ingredient, quantity: float, unitName: str):
        # ผูกออบเจกต์วัตถุดิบหลักเข้ากับตัวแปรสูตร
        self.ingredient = ingredient
        # แปลงข้อมูลปริมาณเป็นทศนิยมเพื่อคำนวณสัดส่วน
        self.quantity = float(quantity)
        # เก็บบันทึกข้อความหน่วยวัดของสัดส่วน
        self.unitName = unitName
        
    @property
    def recipeName(self) -> str:
        # ดึงข้อความชื่อวัตถุดิบออกมาจาก Ingredient Object โดยตรง
        return self.ingredient.name

    def to_dict(self) -> dict:
        # แปลงสูตรนี้เป็น Dictionary สำหรับส่งข้อมูลผ่าน API
        return {
            "ingredient": self.ingredient.to_dict(), # แปลงข้อมูลวัตถุดิบตัวใน
            "recipeName": self.recipeName,           # ดึงชื่อวัตถุดิบหลัก
            "quantity": self.quantity,               # ดึงข้อมูลปริมาณ
            "unitName": self.unitName                 # ดึงข้อความหน่วยวัด
        }