from Classes.Being import Being
from Classes.Food import Food

class Cook(Being):

    def __init__(self, name, position):
        super().__init__(name, 2, "Assets/Other/kucharz.png", position)

        self.current_order = None
        self.available_food = []
        self.available_counters = [[0,4], [1,4], [1,5], [1,6], [1,7], [0,7]]
        self.food_to_make = []
    
    def takeOrderFromWaiter(self, kelner):
        for i in kelner.order_list:
            self.food_to_make.append(i.what_food)

    def makeFood(self, kelner):
        for i in self.food_to_make:
            jedzenie = Food(i, self.available_counters[0])
            self.available_counters.pop(0)
            self.available_food.append(jedzenie)
        
