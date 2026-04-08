import os
import numpy as np

from Classes.Core.Object.Being import Being
from Classes.Objects.Beings.Client import Client
from Classes.Objects.Beings.Cook import Cook
from Classes.Objects.Static.Food import Food
from Classes.Objects.Static.OrderList import OrderList
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
		if abs(self._position[0] - client.getPosition()[0]) + abs(self._position[1] - client.getPosition()[1]) == 1:
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


	def giveOrderList(self, cook: Cook, order_list: OrderList) -> None:
		if not self._order_list or self._order_list_sent:
			return

		if self._position[0] == order_list.getPosition()[0] and self._position[1] == order_list.getPosition()[1]:
			cook.takeOrderFromWaiter(self)
			self._order_list_sent = True
			print("Waiter gave order list to cook")


	def completeOrder(self, client: Client) -> bool:
		if abs(self._position[0] - client.getPosition()[0]) + abs(self._position[1] - client.getPosition()[1]) == 1:
			self._order_list.pop(self._order_list.index((client, client.getFoodName())))
			client.receiveFood()
			print(f"Client at {client.getPosition()} received their food: {client.getFoodName()}")
			return True
		return False


	def getOrderList(self) -> list[Client, Food]:
		return self._order_list

	def _deliver_food(self, clients, collisions_objects, walls) -> None:
		delivery_food = None
		delivery_client = None
		for food in self._carrying:
			for client in clients:
				if client.getFoodName() == food.getName() and client._waiting_for_food:
					delivery_food = food
					delivery_client = client
					break
			if delivery_food is not None:
				break

		if delivery_client is not None:
			self.goTo(delivery_client, collisions_objects, walls)
			if self.completeOrder(delivery_client):
				self._carrying.remove(delivery_food)
				delivery_client.finishEating()
		else:
			self._path = []

	def decide(self, clients, cook: Cook, order_list: OrderList, collisions_objects, walls) -> None:
		all_waiting = len(clients) > 0 and all(client._waiting_for_food for client in clients)

		if all_waiting and len(self.getOrderList()) > 0 and not self._order_list_sent:
			self.goTo(order_list, collisions_objects, walls)
			self.giveOrderList(cook, order_list)
			return

		if cook.hasAvailableFood():
			self.goTo(cook, collisions_objects, walls)
			self.takeFood(cook)
			return

		if self._carrying:
			self._deliver_food(clients, collisions_objects, walls)
			return

		for client in clients:
			if client._wants_to_order:
				self.goTo(client, collisions_objects, walls)
				self.receiveOrder(client)
				return
	