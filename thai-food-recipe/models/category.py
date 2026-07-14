class Category:
    ONE_DISH = "ข้าวจานเดียว"
    NOODLE = "ก๋วยเตี๋ยว"
    SOUP_CURRP = "แกง/ซุป"
    
    @classmethod
    def get_all_categories(cls):
        return [cls.ONE_DISH, cls.NOODLE, cls.SOUP_CURRP]
    
    @classmethod
    def is_valid(cls, category_name: str) -> bool:
        return category_name in cls.get_all_categories()