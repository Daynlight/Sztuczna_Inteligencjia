import os
import numpy as np

from Classes.Core.Object.Being import Being

from Classes.Objects.Static.Food import Food
from Classes.Objects.Static.Counter import Counter
import Classes.Objects.TextureManager as TextureManager










class Cook(Being):
	def __init__(self, position: np.ndarray[int], offset: np.array = [0, 0]):
		super().__init__(render_order=2, 
									 	 texture=TextureManager.COOK_TEXTURE,
										 position=position, offset=offset, size=[1, 2])
		self._current_order: Food = None
		# self._available_counters: list[Counter] = counters
		self._available_food: list[Food] = []
		self._food_to_make: list[Food] = []
    
	
	def takeOrderFromWaiter(self, waiter) -> None:
		for i in waiter.getOrderList():
			self._food_to_make.append(i.getFoodName())


	def makeFood(self) -> None:
		# for i in self._food_to_make:
			# food = Food(i, self._available_counters[0])
			# self._available_counters.pop(0)
			# self._available_food.append(food)
		pass
        

	def getAvailableFood(self) -> Food:
		# return self._available_food.pop(0)
		pass
