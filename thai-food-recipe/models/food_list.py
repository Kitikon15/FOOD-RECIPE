from typing import List
from models.category import Category
from models.food import Food
from models.ingredient import Ingredient
from models.recipe import Recipe

# Ingredient cache to reuse Ingredient objects
_ingredients_cache = {}

def get_ingredient(name: str) -> Ingredient:
    if name not in _ingredients_cache:
        _ingredients_cache[name] = Ingredient(name)
    return _ingredients_cache[name]

def populate_recipe_and_price(food: Food):
    """
    Populates recipe details and sets realistic prices based on the food category and ingredients.
    """
    name = food.nameTH
    
    # 1. Determine base price
    base_price = 50.0
    if food.category == Category.ONE_DISH:
        base_price = 50.0
        # Premium proteins increase price
        if any(keyword in name for keyword in ["ทะเล", "กุ้ง", "ปู", "หมูกรอบ", "เป็ดย่าง", "แฮมชีส", "คอหมูย่าง", "ปลาหมึก"]):
            base_price = 65.0
        elif any(keyword in name for keyword in ["เนื้อ", "หมูป่า"]):
            base_price = 60.0
    elif food.category == Category.NOODLE:
        base_price = 50.0
        if any(keyword in name for keyword in ["ทะเล", "กุ้ง", "ปู", "หมูกรอบ"]):
            base_price = 65.0
    elif food.category == Category.SOUP_CURRY:
        base_price = 80.0
        if any(keyword in name for keyword in ["กุ้ง", "รวมมิตร", "กระดูกอ่อน", "เป็ดย่าง", "คอหมูย่าง", "หมูกรอบ"]):
            base_price = 100.0
        elif any(keyword in name for keyword in ["ไข่ตุ๋น", "ไข่พะโล้"]):
            base_price = 60.0

    food.price = base_price

    # 2. Extract protein name
    protein = "เนื้อหมู"
    if "ไก่" in name:
        protein = "เนื้อไก่"
    elif "หมูกรอบ" in name:
        protein = "หมูกรอบ"
    elif "ทะเล" in name:
        protein = "อาหารทะเล"
    elif "กุ้ง" in name:
        protein = "กุ้งสด"
    elif "ปู" in name:
        protein = "เนื้อปู"
    elif "เนื้อ" in name:
        protein = "เนื้อวัว"
    elif "หมูป่า" in name:
        protein = "เนื้อหมูป่า"
    elif "เป็ดย่าง" in name:
        protein = "เป็ดย่าง"
    elif "ปลาหมึก" in name:
        protein = "ปลาหมึก"
    elif "ไข่เจียว" in name:
        protein = "ไข่ไก่"
    elif "หอยขม" in name:
        protein = "เนื้อหอยขม"
    elif "กระดูกอ่อน" in name:
        protein = "กระดูกอ่อนหมู"
    elif "ปลา" in name:
        protein = "เนื้อปลา"

    # 3. Add ingredients based on recipes (Matching the 6 recipes from user images + dynamic recipes)
    
    # --- RECIPE 1: คั่วพริกเกลือ (e.g. หมูกรอบผัดพริกเกลือ) ---
    if "พริกเกลือ" in name:
        food.add_recipe(Recipe(get_ingredient(protein), 150.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("รากผักชีสับละเอียด"), 5.0, "ราก"))
        food.add_recipe(Recipe(get_ingredient("กระเทียมสับ"), 5.0, "กลีบ"))
        food.add_recipe(Recipe(get_ingredient("พริกขี้หนูสับหยาบ"), 10.0, "เม็ด"))
        food.add_recipe(Recipe(get_ingredient("เกลือ"), 0.5, "ช้อนชา"))
        food.add_recipe(Recipe(get_ingredient("ผงปรุงรส"), 1.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("ผักชีซอย"), 1.0, "ต้น"))

    # --- RECIPE 2: กะเพราแห้ง ---
    elif "กะเพรา" in name:
        if "ไข่เยี่ยวม้า" in name:
            food.add_recipe(Recipe(get_ingredient("ไข่เยี่ยวม้า"), 2.0, "ฟอง"))
            food.add_recipe(Recipe(get_ingredient("หมูสับ"), 80.0, "กรัม"))
        else:
            food.add_recipe(Recipe(get_ingredient(protein), 150.0, "กรัม"))
            
        food.add_recipe(Recipe(get_ingredient("พริกสด"), 6.0, "เม็ด"))
        food.add_recipe(Recipe(get_ingredient("กระเทียมกลีบเล็ก"), 2.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("น้ำมันพืช"), 2.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("พริกไทยป่น"), 1.0, "ช้อนชา"))
        food.add_recipe(Recipe(get_ingredient("ผงปรุงรส"), 0.5, "ช้อนชา"))
        food.add_recipe(Recipe(get_ingredient("น้ำตาลทราย"), 1.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("ซอสหอยนางรม"), 1.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("ซอสปรุงรส"), 0.5, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("ใบกะเพรา"), 1.0, "กำ"))

    # --- RECIPE 3: ผัดกระเทียมพริกไทย ---
    elif "กระเทียม" in name:
        food.add_recipe(Recipe(get_ingredient(protein), 150.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("กระเทียมสับ"), 0.5, "ถ้วยตวง"))
        food.add_recipe(Recipe(get_ingredient("น้ำมันหอย"), 1.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("ซีอิ๊วขาว"), 2.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("น้ำตาล"), 1.0, "ช้อนชา"))
        food.add_recipe(Recipe(get_ingredient("น้ำมันพืช"), 1.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("พริกไทย"), 1.0, "ช้อนชา"))
        food.add_recipe(Recipe(get_ingredient("ผักชี"), 1.0, "ต้น"))

    # --- RECIPE 4: ผัดขี้เมา ---
    elif "ขี้เมา" in name:
        if "มาม่า" in name:
            food.add_recipe(Recipe(get_ingredient("บะหมี่กึ่งสำเร็จรูป"), 1.0, "ซอง"))
            food.add_recipe(Recipe(get_ingredient("เนื้อสัตว์รวม"), 100.0, "กรัม"))
        else:
            food.add_recipe(Recipe(get_ingredient(protein), 150.0, "กรัม"))
            
        food.add_recipe(Recipe(get_ingredient("พริกไทยสด"), 2.5, "พวง"))
        food.add_recipe(Recipe(get_ingredient("พริกชี้ฟ้าแดง"), 4.0, "เม็ด"))
        food.add_recipe(Recipe(get_ingredient("กระเทียมสับ"), 4.0, "กลีบ"))
        food.add_recipe(Recipe(get_ingredient("ข้าวโพดอ่อน"), 5.0, "ฝัก"))
        food.add_recipe(Recipe(get_ingredient("ใบมะกรูด"), 5.0, "ใบ"))
        food.add_recipe(Recipe(get_ingredient("ใบกะเพรา"), 1.0, "กำ"))
        food.add_recipe(Recipe(get_ingredient("น้ำตาลทราย"), 0.5, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("น้ำมันหอย"), 1.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("น้ำเปล่า"), 0.5, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("น้ำมันพืช"), 1.0, "ช้อนโต๊ะ"))

    # --- RECIPE 5: ผัดผงกะหรี่ ---
    elif "ผงกะหรี่" in name:
        food.add_recipe(Recipe(get_ingredient(protein), 150.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("ผงกะหรี่"), 2.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("น้ำพริกเผา"), 1.5, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("กระเทียมสับ"), 1.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("ซอสปรุงรส"), 0.5, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("น้ำตาลทราย"), 1.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("ซีอิ๊วขาว"), 1.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("ซอสเห็ดหอม"), 3.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("นมข้นจืด"), 0.5, "ถ้วยตวง"))
        food.add_recipe(Recipe(get_ingredient("น้ำเปล่า"), 0.25, "ถ้วยตวง"))
        food.add_recipe(Recipe(get_ingredient("น้ำมันพืช"), 1.0, "ช้อนโต๊ะ"))

    # --- RECIPE 6: ผัดพริกแกง / พะแนง / แกงป่า / ผัดเผ็ด ---
    elif any(keyword in name for keyword in ["พริกแกง", "พะแนง", "แกงเผ็ด", "แกงป่า", "ผัดเผ็ด", "ผัดฉ่า"]):
        food.add_recipe(Recipe(get_ingredient(protein), 150.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("ถั่วฝักยาวหั่น"), 1.0, "ถ้วย"))
        food.add_recipe(Recipe(get_ingredient("น้ำมันพืช"), 2.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("น้ำพริกแกงเผ็ด" if "พริกแกง" in name or "ผัดเผ็ด" in name or "แกงเผ็ด" in name else "พริกแกงเฉพาะสูตร"), 1.5, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("น้ำปลา"), 1.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("น้ำตาลทราย"), 0.5, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("ใบมะกรูดซอย"), 3.0, "ใบ"))
        food.add_recipe(Recipe(get_ingredient("พริกชี้ฟ้าแดง"), 1.0, "เม็ด"))

    # --- OTHER DYNAMIC RECIPES ---
    
    # 7. ข้าวผัดประเภทต่างๆ
    elif "ข้าวผัด" in name:
        food.add_recipe(Recipe(get_ingredient(protein), 150.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("ข้าวสวย"), 1.0, "จาน"))
        food.add_recipe(Recipe(get_ingredient("ไข่ไก่"), 1.0, "ฟอง"))
        food.add_recipe(Recipe(get_ingredient("กระเทียมสับ"), 1.0, "ช้อนชา"))
        food.add_recipe(Recipe(get_ingredient("หอมใหญ่หั่นแว่น"), 0.25, "หัว"))
        if "ไข่เค็ม" in name:
            food.add_recipe(Recipe(get_ingredient("ไข่แดงเค็ม"), 2.0, "ฟอง"))
        elif "อเมริกัน" in name:
            food.add_recipe(Recipe(get_ingredient("ลูกเกดและถั่วลันเตา"), 1.0, "ช้อนโต๊ะ"))
            food.add_recipe(Recipe(get_ingredient("ซอสมะเขือเทศ"), 2.0, "ช้อนโต๊ะ"))
            food.add_recipe(Recipe(get_ingredient("น่องไก่ทอดและไส้กรอก"), 1.0, "จาน"))
        food.add_recipe(Recipe(get_ingredient("ซีอิ๊วขาว"), 1.5, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("น้ำมันพืช"), 1.0, "ช้อนโต๊ะ"))

    # 8. ผัดผัก / ผัดขิง
    elif "ผัดขิง" in name:
        food.add_recipe(Recipe(get_ingredient(protein), 150.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("ขิงซอย"), 0.5, "ถ้วยตวง"))
        food.add_recipe(Recipe(get_ingredient("เห็ดหูหนู"), 4.0, "ดอก"))
        food.add_recipe(Recipe(get_ingredient("ต้นหอมหั่นท่อน"), 2.0, "ต้น"))
        food.add_recipe(Recipe(get_ingredient("เต้าเจี้ยว"), 1.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("ซอสปรุงรส"), 1.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("น้ำมันพืช"), 1.0, "ช้อนโต๊ะ"))
        
    elif "ผัดคะน้า" in name:
        food.add_recipe(Recipe(get_ingredient("คะน้าฮ่องกง"), 150.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient(protein), 100.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("พริกขี้หนูทุบ"), 5.0, "เม็ด"))
        food.add_recipe(Recipe(get_ingredient("กระเทียมทุบ"), 4.0, "กลีบ"))
        food.add_recipe(Recipe(get_ingredient("ซอสหอยนางรม"), 1.5, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("เต้าเจี้ยว"), 1.0, "ช้อนชา"))

    # 9. ข้าวมันไก่ / ข้าวหมูแดง / ข้าวขาหมู
    elif "ข้าวมันไก่" in name:
        food.add_recipe(Recipe(get_ingredient("ข้าวหอมมะลิ (หุงข้าวมัน)"), 1.0, "จาน"))
        food.add_recipe(Recipe(get_ingredient("เนื้อไก่ต้ม" if "ทอด" not in name else "ไก่ชุบแป้งทอด"), 150.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("แตงกวาฝาน"), 3.0, "ชิ้น"))
        food.add_recipe(Recipe(get_ingredient("น้ำจิ้มเต้าเจี้ยวสูตรพิเศษ"), 2.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("น้ำซุปโครงไก่"), 1.0, "ถ้วย"))
        
    elif "ข้าวหมูแดง" in name or "ข้าวหมูกรอบ" in name:
        food.add_recipe(Recipe(get_ingredient("ข้าวสวย"), 1.0, "จาน"))
        if "หมูแดง" in name:
            food.add_recipe(Recipe(get_ingredient("หมูแดงสไลด์"), 80.0, "กรัม"))
        if "หมูกรอบ" in name:
            food.add_recipe(Recipe(get_ingredient("หมูกรอบสไลด์"), 80.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("กุนเชียงทอด"), 3.0, "ชิ้น"))
        food.add_recipe(Recipe(get_ingredient("ไข่ต้มยางมะตูม"), 0.5, "ฟอง"))
        food.add_recipe(Recipe(get_ingredient("น้ำราดหมูแดงรสเข้มข้น"), 3.0, "ช้อนโต๊ะ"))
        
    elif "ข้าวขาหมู" in name:
        food.add_recipe(Recipe(get_ingredient("ข้าวสวย"), 1.0, "จาน"))
        food.add_recipe(Recipe(get_ingredient("เนื้อขาหมูพะโล้เปื่อย"), 120.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("คักคึก (ผักกาดดอง)"), 1.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("ผักคะน้าต้ม"), 2.0, "ชิ้น"))
        food.add_recipe(Recipe(get_ingredient("น้ำจิ้มส้มพริกเหลือง"), 1.0, "ช้อนโต๊ะ"))

    # 10. ไข่เจียว / ไข่ข้น
    elif "ไข่เจียว" in name:
        food.add_recipe(Recipe(get_ingredient("ไข่ไก่"), 2.0, "ฟอง"))
        food.add_recipe(Recipe(get_ingredient("ข้าวสวย"), 1.0, "จาน"))
        if "หมูสับ" in name:
            food.add_recipe(Recipe(get_ingredient("หมูสับ"), 50.0, "กรัม"))
        elif "กุ้ง" in name:
            food.add_recipe(Recipe(get_ingredient("กุ้งสับ"), 50.0, "กรัม"))
        elif "แหนม" in name:
            food.add_recipe(Recipe(get_ingredient("แหนมบด"), 50.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("ซีอิ๊วขาว"), 1.0, "ช้อนชา"))
        food.add_recipe(Recipe(get_ingredient("น้ำมันพืชสำหรับทอด"), 3.0, "ช้อนโต๊ะ"))

    elif "ไข่ข้น" in name:
        food.add_recipe(Recipe(get_ingredient("ไข่ไก่"), 2.0, "ฟอง"))
        food.add_recipe(Recipe(get_ingredient("ข้าวสวย"), 1.0, "จาน"))
        if "กุ้ง" in name:
            food.add_recipe(Recipe(get_ingredient("กุ้งสด"), 3.0, "ตัว"))
        elif "หมู" in name:
            food.add_recipe(Recipe(get_ingredient("เนื้อหมูสไลด์"), 50.0, "กรัม"))
        elif "แฮมชีส" in name:
            food.add_recipe(Recipe(get_ingredient("แฮมหั่นเต๋า"), 30.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient("มอสซาเรลล่าชีส"), 20.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("นมสดจืด"), 2.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("เนยจืด"), 1.0, "ช้อนโต๊ะ"))

    # 11. ผัดซีอิ๊ว / ผัดไทย / ราดหน้า (เมนูเส้นผัด)
    elif any(keyword in name for keyword in ["ผัดซีอิ๊ว", "ผัดไทย", "ราดหน้า", "คั่วไก่", "คั่วทะเล"]):
        if "ผัดไทย" in name:
            food.add_recipe(Recipe(get_ingredient("เส้นจันท์"), 120.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient(protein), 100.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient("ใบกุยช่ายและถั่วงอก"), 50.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient("เต้าหู้เหลืองหั่นเต๋า"), 20.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient("น้ำซอสผัดไทยสูตรมะขามเปียก"), 2.0, "ช้อนโต๊ะ"))
            food.add_recipe(Recipe(get_ingredient("ถั่วลิสงป่น"), 1.0, "ช้อนโต๊ะ"))
        elif "ราดหน้า" in name:
            food.add_recipe(Recipe(get_ingredient("เส้นใหญ่"), 120.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient(protein), 100.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient("ยอดคะน้า"), 50.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient("เต้าเจี้ยวบด"), 1.0, "ช้อนโต๊ะ"))
            food.add_recipe(Recipe(get_ingredient("แป้งมันฮ่องกง (ทำน้ำราด)"), 1.5, "ช้อนโต๊ะ"))
            food.add_recipe(Recipe(get_ingredient("น้ำซุปกระดูกหมู"), 1.0, "ถ้วย"))
        elif "คั่ว" in name:
            food.add_recipe(Recipe(get_ingredient("เส้นใหญ่"), 120.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient(protein), 100.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient("ไข่ไก่"), 1.0, "ฟอง"))
            food.add_recipe(Recipe(get_ingredient("ผักกาดหอม"), 20.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient("ซีอิ๊วขาวและพริกไทย"), 1.0, "ช้อนโต๊ะ"))
        else:  # ผัดซีอิ๊ว
            food.add_recipe(Recipe(get_ingredient("เส้นใหญ่" if "ใหญ่" in name or "หมี่" not in name else "เส้นหมี่"), 120.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient(protein), 100.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient("ผักคะน้า"), 50.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient("ไข่ไก่"), 1.0, "ฟอง"))
            food.add_recipe(Recipe(get_ingredient("ซีอิ๊วดำหวาน"), 1.0, "ช้อนโต๊ะ"))
            food.add_recipe(Recipe(get_ingredient("น้ำมันหอย"), 1.0, "ช้อนโต๊ะ"))
            food.add_recipe(Recipe(get_ingredient("น้ำมันพืช"), 1.0, "ช้อนโต๊ะ"))

    # 12. สุกี้
    elif "สุกี้" in name:
        food.add_recipe(Recipe(get_ingredient("วุ้นเส้น"), 80.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient(protein), 100.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("ผักกาดขาวและผักบุ้งจีน"), 100.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("ไข่ไก่"), 1.0, "ฟอง"))
        food.add_recipe(Recipe(get_ingredient("น้ำจิ้มสุกี้สูตรกวางตุ้ง"), 3.0, "ช้อนโต๊ะ"))
        if "น้ำ" in name:
            food.add_recipe(Recipe(get_ingredient("น้ำซุปผัก"), 1.5, "ถ้วย"))
        else:
            food.add_recipe(Recipe(get_ingredient("น้ำมันพืชสำหรับผัด"), 1.0, "ช้อนโต๊ะ"))

    # 13. ยำ / ตำ
    elif any(keyword in name for keyword in ["ตำ", "ยำ"]):
        if "ตำ" in name:
            food.add_recipe(Recipe(get_ingredient("มะละกอสับและแครอท"), 100.0, "กรัม"))
            if "เส้นเล็ก" in name:
                food.add_recipe(Recipe(get_ingredient("เส้นเล็กต้มหนึบ"), 100.0, "กรัม"))
            elif "ซั่ว" in name:
                food.add_recipe(Recipe(get_ingredient("ขนมจีน"), 100.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient("น้ำปลาร้าต้มสุก"), 2.0, "ช้อนโต๊ะ"))
            food.add_recipe(Recipe(get_ingredient("มะนาว"), 1.0, "ลูก"))
            food.add_recipe(Recipe(get_ingredient("มะเขือเทศสีดา"), 2.0, "ลูก"))
            food.add_recipe(Recipe(get_ingredient("พริกแห้งและกระเทียม"), 1.0, "ช้อนโต๊ะ"))
        else: # ยำ
            if "วุ้นเส้น" in name:
                food.add_recipe(Recipe(get_ingredient("วุ้นเส้นต้ม"), 100.0, "กรัม"))
            elif "มาม่า" in name:
                food.add_recipe(Recipe(get_ingredient("บะหมี่กึ่งสำเร็จรูปต้ม"), 1.0, "ซอง"))
            elif "ขนมจีน" in name:
                food.add_recipe(Recipe(get_ingredient("ขนมจีน"), 150.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient(protein), 100.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient("หอมใหญ่และขึ้นฉ่าย"), 30.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient("มะเขือเทศ"), 0.5, "ลูก"))
            food.add_recipe(Recipe(get_ingredient("น้ำยำสามรส (มะนาว น้ำปลา น้ำตาล)"), 3.0, "ช้อนโต๊ะ"))

    # 14. ต้มยำ / ต้มแซ่บ
    elif "ต้มยำ" in name or "ต้มแซ่บ" in name:
        food.add_recipe(Recipe(get_ingredient(protein), 150.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("สมุนไพรสด (ข่า ตะไคร้ ใบมะกรูด หอมแดง)"), 1.0, "ชุด"))
        food.add_recipe(Recipe(get_ingredient("เห็ดฟาง"), 50.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("พริกขี้หนูสวนบุบ"), 10.0, "เม็ด"))
        food.add_recipe(Recipe(get_ingredient("มะนาว"), 1.5, "ลูก"))
        food.add_recipe(Recipe(get_ingredient("น้ำปลา"), 2.0, "ช้อนโต๊ะ"))
        if "ต้มยำ" in name:
            food.add_recipe(Recipe(get_ingredient("น้ำพริกเผา"), 1.0, "ช้อนโต๊ะ"))
            if "กุ้ง" in name or "รวมมิตร" in name:
                food.add_recipe(Recipe(get_ingredient("นมข้นจืด (สูตรน้ำข้น)"), 2.0, "ช้อนโต๊ะ"))
        elif "ต้มแซ่บ" in name:
            food.add_recipe(Recipe(get_ingredient("ข้าวคั่วและผักชีฝรั่ง"), 1.0, "ช้อนโต๊ะ"))

    # 15. แกงเขียวหวาน
    elif "แกงเขียวหวาน" in name:
        food.add_recipe(Recipe(get_ingredient(protein), 150.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("น้ำพริกแกงเขียวหวาน"), 2.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("กะทิสด"), 1.0, "ถ้วย"))
        food.add_recipe(Recipe(get_ingredient("มะเขือเปราะมะเขือพวง"), 50.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("ใบโหระพาและพริกชี้ฟ้า"), 1.0, "กำ"))
        food.add_recipe(Recipe(get_ingredient("น้ำปลาและน้ำตาลปี๊บ"), 1.0, "ช้อนโต๊ะ"))

    # 16. แกงส้ม
    elif "แกงส้ม" in name:
        if "ชะอมไข่" in name:
            food.add_recipe(Recipe(get_ingredient("ไข่เจียวชะอมหั่นชิ้น"), 100.0, "กรัม"))
            food.add_recipe(Recipe(get_ingredient("กุ้งสด"), 3.0, "ตัว"))
        elif "แป๊ะซะ" in name:
            food.add_recipe(Recipe(get_ingredient("ปลาช่อนทอดกรอบ"), 1.0, "ตัว"))
            food.add_recipe(Recipe(get_ingredient("ผักกาดขาวและผักกระเฉด"), 100.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("พริกแกงส้มใต้"), 2.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("น้ำมะขามเปียก"), 3.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("น้ำปลาและน้ำตาลปี๊บ"), 1.5, "ช้อนโต๊ะ"))

    # 17. ต้มจืด / แกงจืด
    elif "ต้มจืด" in name or "แกงจืด" in name:
        food.add_recipe(Recipe(get_ingredient("เต้าหู้หลอดไข่"), 1.0, "หลอด"))
        food.add_recipe(Recipe(get_ingredient("หมูสับ"), 80.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("ผักกาดขาว"), 100.0, "กรัม"))
        if "วุ้นเส้น" in name:
            food.add_recipe(Recipe(get_ingredient("วุ้นเส้นต้ม"), 50.0, "กรัม"))
        elif "ตำลึง" in name:
            food.add_recipe(Recipe(get_ingredient("ใบตำลึง"), 50.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("ซีอิ๊วขาวและผงปรุงรสหมู"), 1.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("กระเทียมเจียวผักชี"), 1.0, "ช้อนชา"))

    # 18. ไข่ตุ๋น / ไข่พะโล้
    elif "ไข่ตุ๋น" in name:
        food.add_recipe(Recipe(get_ingredient("ไข่ไก่"), 3.0, "ฟอง"))
        food.add_recipe(Recipe(get_ingredient("หมูสับและต้นหอม"), 30.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("น้ำซุป"), 1.0, "ถ้วย"))
        food.add_recipe(Recipe(get_ingredient("ซีอิ๊วขาว"), 1.0, "ช้อนโต๊ะ"))
    elif "ไข่พะโล้" in name:
        food.add_recipe(Recipe(get_ingredient("ไข่เป็ดต้มปอกเปลือก"), 3.0, "ฟอง"))
        food.add_recipe(Recipe(get_ingredient("หมูสามชั้น"), 100.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("เต้าหู้ดำพะโล้"), 4.0, "ชิ้น"))
        food.add_recipe(Recipe(get_ingredient("ผงพะโล้และเครื่องเทศ"), 1.0, "ซอง"))
        food.add_recipe(Recipe(get_ingredient("น้ำตาลปี๊บและซีอิ๊วดำหวาน"), 2.0, "ช้อนโต๊ะ"))

    # 19. ไก่ทอด / หมูทอด / คอหมูย่าง
    elif any(keyword in name for keyword in ["ทอดเกลือ", "ทอดน้ำปลา", "ย่างน้ำจิ้มแจ่ว"]):
        food.add_recipe(Recipe(get_ingredient(protein), 200.0, "กรัม"))
        if "เกลือ" in name:
            food.add_recipe(Recipe(get_ingredient("เกลือป่น"), 1.0, "ช้อนชา"))
        elif "น้ำปลา" in name:
            food.add_recipe(Recipe(get_ingredient("น้ำปลาแท้เกรดพรีเมียม"), 1.5, "ช้อนโต๊ะ"))
        elif "น้ำจิ้มแจ่ว" in name:
            food.add_recipe(Recipe(get_ingredient("ข้าวคั่ว พริกป่น น้ำขามเปียก"), 1.0, "ชุด"))
        food.add_recipe(Recipe(get_ingredient("แป้งทอดกรอบ (สำหรับทอด)"), 1.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("น้ำมันพืชสำหรับทอด/ย่าง"), 3.0, "ช้อนโต๊ะ"))

    # 20. default fallback
    else:
        food.add_recipe(Recipe(get_ingredient(protein), 150.0, "กรัม"))
        food.add_recipe(Recipe(get_ingredient("กระเทียมสดสับ"), 1.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("น้ำมันพืช"), 1.0, "ช้อนโต๊ะ"))
        food.add_recipe(Recipe(get_ingredient("เครื่องปรุงรสพื้นฐาน (ซีอิ๊ว น้ำตาล น้ำปลา)"), 1.0, "ช้อนโต๊ะ"))


def get_100_thai_foods() -> List[Food]:
    foods = []
    
    # ==========================================
    # หมวดที่ 1: ข้าวจานเดียว (เมนูที่ 1 - 50)
    # ==========================================
    
    one_dish_menus = [
        "ข้าวกะเพราไก่", "ข้าวกะเพราหมู", "ข้าวกะเพราหมูกรอบ", "ข้าวกะเพราทะเล", "ข้าวกะเพราเนื้อ",
        "ข้าวกะเพราไข่เยี่ยวม้า", "ข้าวผัดหมู", "ข้าวผัดไก่", "ข้าวผัดกุ้ง", "ข้าวผัดปู",
        "ข้าวผัดทะเล", "ข้าวผัดพริกแกงหมู", "ข้าวผัดพริกแกงไก่", "ข้าวผัดพริกแกงทะเล", "ข้าวผัดน้ำพริกเผา",
        "ข้าวผัดต้มยำ", "ข้าวผัดอเมริกัน", "ข้าวหมูกระเทียม", "ข้าวไก่กระเทียม", "ข้าวกุ้งกระเทียม",
        "ข้าวหมูทอดน้ำปลา", "ข้าวหมูทอดไข่ดาว", "ข้าวหมูผัดพริกไทยดำ", "ข้าวไก่ผัดพริกไทยดำ", "ข้าวหมูผัดขิง",
        "ข้าวไก่ผัดขิง", "ข้าวหมูผัดพริกหยวก", "ข้าวไก่ผัดเม็ดมะม่วง", "ข้าวหมูผัดเปรี้ยวหวาน", "ข้าวไก่ผัดเปรี้ยวหวาน",
        "ข้าวผัดคะน้าหมูกรอบ", "ข้าวหมูแดง", "ข้าวหมูกรอบ", "ข้าวขาหมู", "ข้าวมันไก่",
        "ข้าวมันไก่ทอด", "ข้าวไข่เจียวหมูสับ", "ข้าวไข่เจียวกุ้ง", "ข้าวไข่เจียวแหนม", "ข้าวไข่ข้นกุ้ง",
        "ข้าวไข่ข้นหมู", "ข้าวไข่ข้นแฮมชีส", "ข้าวราดแกงเขียวหวานไก่", "ข้าวราดพะแนงหมู", "ข้าวราดมัสหมั่นเนื้อ",
        "ข้าวราดแกงเผ็ดเป็ดย่าง", "ข้าวราดแกงป่าไก่", "ข้าวราดผัดฉ่าทะเล", "ข้าวราดผัดเผ็ดหมูป่า", "ข้าวปลาหมึกผัดไข่เค็ม"
    ]
    for menu in one_dish_menus:
        food = Food(nameTh=menu, category=Category.ONE_DISH)
        populate_recipe_and_price(food)
        foods.append(food)
    
    # ==========================================
    # หมวดที่ 2: เมนูเส้น (เมนูที่ 51 - 76)
    # ==========================================
    
    noodle_menus = [
        "ผัดไทย", "ผัดไทยกุ้งสด", "ผัดซีอิ๊วหมู", "ผัดซีอิ๊วไก่", "ผัดซีอิ๊วทะเล",
        "ราดหน้าหมู", "ราดหน้าไก่", "ราดหน้าทะเล", "ก๋วยเตี๋ยวคั่วไก่", "ก๋วยเตี๋ยวคั่วทะเล",
        "มาม่าผัดขี้เมา", "มาม่าผัดต้มยำ", "สุกี้แห้งหมู", "สุกี้แห้งทะเล", "สุกี้น้ำหมู",
        "สุกี้น้ำไก่", "เส้นใหญ่ผัดซีอิ๊ว", "เส้นหมี่ผัดซีอิ๊ว", "เส้นหมี่ผัดกระเฉด", "ผัดหมี่ซั่ว",
        "วุ้นเส้นผัดไข่", "ตำเส้นเล็ก", "ตำซั่ว", "ยำขนมจีน", "ยำวุ้นเส้น", "ยำมาม่า"
    ]
    for menu in noodle_menus:
        food = Food(nameTh=menu, category=Category.NOODLE)
        populate_recipe_and_price(food)
        foods.append(food)

    # ==========================================
    # หมวดที่ 3: ต้ม แกง และอื่นๆ (เมนูที่ 77 - 100)
    # ==========================================

    soup_curry_menus = [
        "ต้มยำกุ้ง", "ต้มยำรวมมิตร", "ต้มแซ่บกระดูกอ่อน", "ต้มจืดเต้าหู้หมูสับ", "ต้มจืดวุ้นเส้น",
        "แกงจืดตำลึงหมูสับ", "แกงเขียวหวานไก่", "แกงพะแนงหมู", "แกงมัสหมั่นเนื้อ", "แกงส้มชะอมไข่",
        "แกงส้มแป๊ะซะ", "แกงป่าหมู", "แกงเลียงกุ้งสด", "แกงเผ็ดหมู", "แกงคั่วหอยขม",
        "แกงไตปลา", "ไข่ตุ๋น", "ไข่พะโล้", "คอหมูย่างน้ำจิ้มแจ่ว", "ไก่ทอดเกลือ",
        "หมูสามชั้นทอดน้ำปลา", "หมูกรอบผัดพริกเกลือ", "หมูสับผัดไข่เค็ม", "กุ้งผัดผงกะหรี่"
    ]
    
    for menu in soup_curry_menus:
        food = Food(nameTh=menu, category=Category.SOUP_CURRY)
        populate_recipe_and_price(food)
        foods.append(food)
        
    return foods