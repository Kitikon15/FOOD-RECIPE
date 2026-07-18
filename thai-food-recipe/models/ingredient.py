# models/ingredient.py

# คลาสสำหรับเก็บข้อมูลชื่อวัตถุดิบเดี่ยว
class Ingredient:
    
    def __init__(self, name: str):
        # บันทึกชื่อวัตถุดิบลงในตัวแปรออบเจกต์
        self.name = name

    def to_dict(self) -> dict:
        # แปลงเป็น Dictionary เพื่อส่งข้อมูลออกทาง API
        return {
            "name": self.name
        }