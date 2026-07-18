from typing import List, Optional
from models.food import Food
from models.food_list import get_100_thai_foods

class FoodManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Singleton pattern to share food items across requests
        if not cls._instance:
            cls._instance = super(FoodManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.foods: List[Food] = get_100_thai_foods()
        self._initialized = True

    def get_all_foods(self) -> List[Food]:
        return self.foods

    def get_foods_by_category(self, category: str) -> List[Food]:
        return [f for f in self.foods if f.category == category]

    def search_foods(self, query: str) -> List[Food]:
        if not query:
            return self.foods
        
        query = query.lower().strip()
        results = []
        for food in self.foods:
            # Match food name
            if query in food.nameTH.lower():
                results.append(food)
                continue
            
            # Match ingredient name
            for recipe_item in food.recipeList:
                if query in recipe_item.recipeName.lower():
                    results.append(food)
                    break
        return results

    def get_food_by_name(self, name: str) -> Optional[Food]:
        for food in self.foods:
            if food.nameTH == name:
                return food
        return None

    def get_popular_foods(self, limit: int = 6) -> List[Food]:
        # Sort by popularity desc, then by name
        sorted_foods = sorted(self.foods, key=lambda f: (-f.popularity, f.nameTH))
        return sorted_foods[:limit]
