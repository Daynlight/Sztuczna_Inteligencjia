import os
import time
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
		self._carrying: list[Food] = []
		self._order_list: list[Client, Food] = []
		self._order_list_sent: bool = False
    

	def receiveOrder(self, client: Client) -> None:
		for i in range(-1, 2):
			for j in range(-1, 2):
				if i!=j and self._position[0] + i == client.getPosition()[0] and self._position[1] + j == client.getPosition()[1]:
					time.sleep(0.7)
					self._order_list.append((client, client.getFoodName()))
					client.waitForFood()
					self._order_list_sent = False
					print(f"Waiter received order from client at {client.getPosition()}: {client.getFoodName()}")
					return


	def takeFood(self, cook: Cook) -> None:
		if abs(self._position[0] - cook.getPosition()[0]) + abs(self._position[1] - cook.getPosition()[1]) == 1:
			if cook.hasAvailableFood():
				food = cook.getAvailableFood()
				if food:
					self._carrying.append(food)
					print(f"Waiter took {food.getName()} from cook")


	def giveOrderListToCook(self, cook: Cook) -> None:
		if not self._order_list or self._order_list_sent:
			return

		if abs(self._position[0] - cook.getPosition()[0]) + abs(self._position[1] - cook.getPosition()[1]) == 1:
			cook.takeOrderFromWaiter(self)
			self._order_list_sent = True
			print("Waiter gave order list to cook")


	def completeOrder(self, client: Client) -> bool:
		for i in range(-1, 2):
			for j in range(-1, 2):
				if i!=j and self._position[0] + i == client.getPosition()[0] and self._position[1] + j == client.getPosition()[1]:
					time.sleep(0.7)
					self._order_list.pop(self._order_list.index((client, client.getFoodName())))
					client.receiveFood()
					print(f"Client at {client.getPosition()} received their food: {client.getFoodName()}")
					return True
		return False


	def getOrderList(self) -> list[Client, Food]:
		return self._order_list
	