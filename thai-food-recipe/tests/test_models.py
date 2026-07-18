import unittest
from models.category import Category
from models.ingredient import Ingredient
from models.recipe import Recipe
from models.food import Food
from models.order import Order, OrderItem

class TestModels(unittest.TestCase):
    
    def test_category_validation(self):
        self.assertTrue(Category.is_valid("ข้าวจานเดียว"))
        self.assertTrue(Category.is_valid("ก๋วยเตี๋ยว"))
        self.assertTrue(Category.is_valid("แกง/ซุป"))
        self.assertFalse(Category.is_valid("ของหวาน"))
        self.assertFalse(Category.is_valid("เครื่องดื่ม"))

    def test_ingredient_creation(self):
        ing = Ingredient("กะเพรา")
        self.assertEqual(ing.name, "กะเพรา")
        self.assertEqual(ing.to_dict(), {"name": "กะเพรา"})

    def test_recipe_creation(self):
        ing = Ingredient("กระเทียม")
        recipe = Recipe(ing, 5.0, "กลีบ")
        self.assertEqual(recipe.recipeName, "กระเทียม")
        self.assertEqual(recipe.quantity, 5.0)
        self.assertEqual(recipe.unitName, "กลีบ")
        
        recipe_dict = recipe.to_dict()
        self.assertEqual(recipe_dict["recipeName"], "กระเทียม")
        self.assertEqual(recipe_dict["quantity"], 5.0)
        self.assertEqual(recipe_dict["unitName"], "กลีบ")

    def test_food_creation_and_recipe(self):
        food = Food("ข้าวกะเพราไก่", Category.ONE_DISH, price=55.0)
        self.assertEqual(food.nameTH, "ข้าวกะเพราไก่")
        self.assertEqual(food.price, 55.0)
        self.assertEqual(food.popularity, 0)
        
        ing = Ingredient("ใบกะเพรา")
        recipe = Recipe(ing, 1.0, "กำ")
        food.add_recipe(recipe)
        
        self.assertEqual(len(food.recipeList), 1)
        self.assertEqual(food.recipeList[0].recipeName, "ใบกะเพรา")

        # Invalid category should raise ValueError
        with self.assertRaises(ValueError):
            Food("เมนูเสีย", "ประเภทไม่มีอยู่จริง")

    def test_order_and_order_item(self):
        food1 = Food("ข้าวกะเพราหมูกรอบ", Category.ONE_DISH, price=65.0)
        food2 = Food("ต้มยำกุ้ง", Category.SOUP_CURRY, price=100.0)
        
        item1 = OrderItem(food1, 2) # Subtotal: 130.0
        item2 = OrderItem(food2, 1) # Subtotal: 100.0
        
        self.assertEqual(item1.subtotal, 130.0)
        self.assertEqual(item2.subtotal, 100.0)
        
        order = Order("ORD-TEST", [item1, item2], payment_method="PromptPay")
        self.assertEqual(order.total_price, 230.0)
        self.assertEqual(order.status, "pending")
        
        # Test payment updates status and popularity
        order.mark_as_paid()
        self.assertEqual(order.status, "paid")
        self.assertEqual(food1.popularity, 2)
        self.assertEqual(food2.popularity, 1)

if __name__ == '__main__':
    unittest.main()
