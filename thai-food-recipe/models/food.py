from models.category import Category
from models.recipe import Recipe

class Food:
    def __init__(self, nameTh: str, category: str):
        if not Category.is_valid(category):
            raise ValueError(f"ประเภทอาหาร '{category}' ไม่ถูกต้องตามระบบ")
        
        self.nameTH=nameTh
        self.category=category
        self.recipeList=[]
        
    def add_recipe(self, recipe: Recipe):
        if isinstance(recipe, Recipe):
            self.recipeList.append(recipe)
        else:
            raise TypeError
    def display(self):
        print(f"============= {self.nameTH} =============")
        print(f"เมนู: {self.nameTH}")
        print(f"หมวดหมู๋: {self.category}")
        print(f"============= {self.nameTH} =============")
        print("วัตถุดิบที่ใช้:")
        if not self.recipeList:
            print(" -ไม่มีวัตถุดิบที่ใช้")
        for idx, item in enumerate(self.recipeList, start=1):
            print(f"  {idx}. {item.recipeName:<22} {item.quantity:>6} {item.unitName}")
        print(f"============= {self.nameTH} =============")