import os
import numpy as np

from Classes.Core.Object.Being import Being

from Classes.Objects.Static.Food import Food
from Classes.Objects.Static.Counter import Counter
import Classes.Objects.TextureManager as TextureManager
from Classes.Core.Animation.Animation import Animation
from Classes.Core.Animation.Frame import Frame

from conf import DEBUG










class Cook(Being):
	def __init__(self, position: np.ndarray[int], counters: np.ndarray[Counter], offset: np.array = [0, 0]):
		super().__init__(render_order=2, 
									 	 texture=TextureManager.COOK1_TEXTURE,
										 position=position, offset=offset, size=[1, 2])
		self._current_order: Food = None
		self._available_counters: list[Counter] = [i.getPosition() for i in counters]
		self._available_food: list[Food] = []
		self._food_to_make: list[Food] = []
		self.setAnimation("Idle", Animation([Frame(TextureManager.COOK1_TEXTURE, 1), 
																			   Frame(TextureManager.COUNTER_TEXTURE, 2)]))
		self.setState("Idle")
    
	
	def hasAvailableFood(self) -> bool:
		return len(self._available_food) > 0

	def hasPendingOrders(self) -> bool:
		return len(self._food_to_make) > 0

	def decide(self) -> None:
		if self._food_to_make:
			self.makeFood()
		
	def takeOrderFromWaiter(self, waiter) -> None:
		for i in waiter.getOrderList():
			self._food_to_make.append(i[1])
		if(DEBUG): print(f"Cook received order list: {[i[1] for i in waiter.getOrderList()]}")


	def makeFood(self) -> None:
		for i in self._food_to_make:
			if(DEBUG): print(f"Cook is making {i}")
			food = Food(i, self._available_counters[0])
			self._available_counters.pop(0)
			self._available_food.append(food)
			if(DEBUG): print(f"Cook finished making {i}")
		self._food_to_make = []
        
				
	def getAvailableFood(self) -> Food:
		if self._available_food:
			self._available_counters.append(self._available_food[0].getPosition())
			return self._available_food.pop(0)
		return None
			