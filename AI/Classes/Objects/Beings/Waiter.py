import os
import numpy as np

from Classes.Core.Object.Being import Being
from Classes.Objects.Beings.Client import Client
from Classes.Objects.Beings.Cook import Cook
from Classes.Objects.Static.Food import Food

import Classes.Objects.TextureManager as TextureManager

from conf import WAITER_VELOCITY









class Waiter(Being):
	def __init__(self, position: np.ndarray[int], offset: np.array = [0, 0]):
		super().__init__(render_order=3, 
									 	 texture=TextureManager.WAITER_TEXTURE,
										 position=position, offset=offset, velocity=WAITER_VELOCITY, size=[1, 2])
		self._carrying_name: list[Food] = None
		self._order_list: list[Client, Food] = []
    

	def receiveOrder(self, client: Client) -> None:
		self._order_list.append(client)


	def takeFood(self, cook: Cook) -> None:
		food_name: str = self._order_list[0].getFoodName()
		self._carrying_name: str = food_name
		cook.getAvailableFood()
		# cook.available_counters.insert(0, ) # TODO: make counters available after taking food


	def completeOrder(self) -> None:
		# orders will be completed in a queue approach for now
		self._order_list[0].receiveFood()
		self._order_list.pop(0)


	def getOrderList(self) -> list[Client, Food]:
		return self._order_list
	