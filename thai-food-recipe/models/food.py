from models.category import Category
from models.recipe import Recipe

class Food:
    def __init__(self, nameTh: str, category: str, price: float = 50.0):
        if not Category.is_valid(category):
            raise ValueError(f"ประเภทอาหาร '{category}' ไม่ถูกต้องตามระบบ")
        
        self.nameTH = nameTh
        self.nameTh = nameTh  # For compatibility with UML/food_list
        self.category = category
        self.recipeList = []
        self.price = float(price)
        self.popularity = 0
        
    def add_recipe(self, recipe: Recipe):
        if isinstance(recipe, Recipe):
            self.recipeList.append(recipe)
        else:
            raise TypeError("ต้องเป็นออบเจกต์ประเภท Recipe เท่านั้น")

    def display(self):
        print(f"============= {self.nameTH} =============")
        print(f"เมนู: {self.nameTH}")
        print(f"หมวดหมู่: {self.category}")
        print(f"ราคา: {self.price} บาท")
        print(f"ยอดสั่งซื้อ: {self.popularity} ครั้ง")
        print(f"============= {self.nameTH} =============")
        print("วัตถุดิบที่ใช้:")
        if not self.recipeList:
            print(" -ไม่มีวัตถุดิบที่ใช้")
        for idx, item in enumerate(self.recipeList, start=1):
            print(f"  {idx}. {item.recipeName:<22} {item.quantity:>6} {item.unitName}")
        print(f"============= {self.nameTH} =============")

    def to_dict(self) -> dict:
        return {
            "nameTh": self.nameTH,
            "category": self.category,
            "price": self.price,
            "popularity": self.popularity,
            "recipeList": [item.to_dict() for item in self.recipeList]
        }