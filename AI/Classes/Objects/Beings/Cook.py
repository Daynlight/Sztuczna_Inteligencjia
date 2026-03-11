import os
import numpy as np

from Classes.Objects.Beings.Being import Being
from Classes.Objects.Static.Food import Food
from Classes.Objects.Static.Counter import Counter

from conf import PATH_TO_ASSETS









class Cook(Being):
	def __init__(self, position: np.ndarray[int], counters: Counter, offset: np.array = [0, 0]):
		super().__init__(2, os.path.join(PATH_TO_ASSETS, "Other", "kucharz.png"), position, offset)
		self._current_order: Food = None
		self._available_counters: list[Counter] = counters
		self._available_food: list[Food] = []
		self._food_to_make: list[Food] = []
    
	
	def takeOrderFromWaiter(self, waiter) -> None:
		for i in waiter.getOrderList():
			self._food_to_make.append(i.getFoodName())


	def makeFood(self) -> None:
		for i in self._food_to_make:
			food = Food(i, self._available_counters[0])
			self._available_counters.pop(0)
			self._available_food.append(food)
        

	def getAvailableFood(self) -> Food:
		return self._available_food.pop(0)
