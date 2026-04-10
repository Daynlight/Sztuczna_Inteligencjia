from Classes.Being import Being
from conf import movementSpeed
import numpy as np

class Waiter(Being):
    def __init__(self, name, position, offset: np.array = [0, 0]):
        super().__init__(name, 3, "Assets/Other/jenkins.png", position, offset, movementSpeed)

        self.carrying_food = False
        self.carrying_name = None
        self.order_list = []
    
    def recieveOrder(self, client):
        self.order_list.append(client)

    def takeFood(self, cook):
        self.carrying_food = True
        food_name = self.order_list[0].what_food
        self.carrying_name = food_name
        cook.available_food.pop(0)
        # cook.available_counters.insert(0, ) # TODO: make counters available after taking food

    def completeOrder(self):
        # orders will be completed in a queue approach for now
        self.order_list[0].recieveFood()
        self.order_list.pop(0)