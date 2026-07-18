# models/category.py

# คลาสเก็บหมวดหมู่และตรวจสอบประเภทอาหาร
class Category:
    # ค่าคงที่สำหรับกำหนดประเภทอาหารแต่ละหมวด
    ONE_DISH = "ข้าวจานเดียว"
    NOODLE = "ก๋วยเตี๋ยว"
    SOUP_CURRY = "แกง/ซุป"

    @classmethod
    def get_all_categories(cls):
        # คืนค่ารายการหมวดหมู่ทั้งหมดในระบบเป็นลิสต์
        return [cls.ONE_DISH, cls.NOODLE, cls.SOUP_CURRY]

    @classmethod
    def is_valid(cls, category_name: str) -> bool:
        # ตรวจสอบคำค้นหาว่าตรงกับลิสต์หมวดหมู่ที่รองรับหรือไม่ (True/False)
        return category_name in cls.get_all_categories()