from models.ingredient import Ingredient

class Recipe:
    def __init__(self, ingredient: Ingredient, quantity: float, unitName: str):
        self.ingredient = ingredient
        self.quantity = float(quantity)
        self.unitName = unitName
        
    @property
    def recipeName(self) -> str:
        return self.ingredient.name

    def to_dict(self) -> dict:
        return {
            "ingredient": self.ingredient.to_dict(),
            "recipeName": self.recipeName,
            "quantity": self.quantity,
            "unitName": self.unitName
        }