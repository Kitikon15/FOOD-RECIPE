class Category:
    ONE_DISH = "ข้าวจานเดียว"
    NOODLE = "ก๋วยเตี๋ยว"
    SOUP_CURRY = "แกง/ซุป"
    
    @classmethod
    def get_all_categories(cls):
        return [cls.ONE_DISH, cls.NOODLE, cls.SOUP_CURRY]
    
    @classmethod
    def is_valid(cls, category_name: str) -> bool:
        return category_name in cls.get_all_categories()