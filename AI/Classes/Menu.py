




class Menu():
    def __init__(self):
        self._available_food: list[str] =  [
            "apple_pie",
            "burger",
            "burrito",
            "cheesecake",
            "chocolate_cake",
            "dumplings",
            "fried_egg",
            "hotdog",
            "pancakes",
            "pizza",
            "roasted_chicken",
            "sandwich",
            "strawberry_cake",
            "taco",
            "waffle"]
    
    def getFoodList(self) -> list[str]:
        return self._available_food