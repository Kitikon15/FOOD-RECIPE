import unittest
from services.food_manager import FoodManager
from services.order_manager import OrderManager
from models.category import Category

class TestServices(unittest.TestCase):
    
    def setUp(self):
        # Reset Singleton state for testing if needed
        self.food_manager = FoodManager()
        self.order_manager = OrderManager()

    def test_food_manager_singleton(self):
        fm2 = FoodManager()
        self.assertIs(self.food_manager, fm2)

    def test_get_all_foods(self):
        foods = self.food_manager.get_all_foods()
        self.assertEqual(len(foods), 100) # Should have exactly 100 dishes

    def test_get_foods_by_category(self):
        one_dish = self.food_manager.get_foods_by_category(Category.ONE_DISH)
        noodles = self.food_manager.get_foods_by_category(Category.NOODLE)
        soup_curry = self.food_manager.get_foods_by_category(Category.SOUP_CURRY)
        
        # Total sum of elements should be 100
        self.assertEqual(len(one_dish) + len(noodles) + len(soup_curry), 100)

    def test_search_foods(self):
        # Search by dish name / ingredient
        results = self.food_manager.search_foods("กะเพรา")
        self.assertTrue(len(results) > 0)
        for food in results:
            name_match = "กะเพรา" in food.nameTH
            ing_match = any("กะเพรา" in item.recipeName for item in food.recipeList)
            self.assertTrue(name_match or ing_match)
            
        # Search by ingredient name (e.g. "เส้นจันท์" in ผัดไทย)
        results2 = self.food_manager.search_foods("เส้นจันท์")
        self.assertTrue(len(results2) > 0)
        
    def test_order_creation_and_payment(self):
        items_data = [
            {"food_name": "ข้าวกะเพราไก่", "quantity": 1},
            {"food_name": "ผัดไทยกุ้งสด", "quantity": 2}
        ]
        
        # Place new order
        order = self.order_manager.create_order(items_data=items_data, payment_method="Credit Card")
        self.assertIsNotNone(order)
        self.assertEqual(order.status, "pending")
        self.assertEqual(order.payment_method, "Credit Card")
        
        # Check that it exists in history
        history = self.order_manager.get_order_history()
        self.assertIn(order, history)
        
        # Verify payment processing updates status and increments popularity
        grapow = self.food_manager.get_food_by_name("ข้าวกะเพราไก่")
        initial_popularity = grapow.popularity
        
        self.order_manager.pay_order(order.order_id)
        self.assertEqual(order.status, "paid")
        self.assertEqual(grapow.popularity, initial_popularity + 1)

if __name__ == '__main__':
    unittest.main()
