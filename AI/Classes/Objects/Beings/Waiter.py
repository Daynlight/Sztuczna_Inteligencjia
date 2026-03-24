import os
import numpy as np

from Classes.Objects.Beings.Being import Being
from Classes.Objects.Beings.Client import Client
from Classes.Objects.Beings.Cook import Cook
from Classes.Objects.Static.Food import Food
from Knowlege.Frame import Frame

from conf import WAITER_VELOCITY, PATH_TO_ASSETS









class Waiter(Being):
	def __init__(self, position: np.ndarray[int], offset: np.array = [0, 0]):
		super().__init__(3, os.path.join(PATH_TO_ASSETS, "Other", "jenkins.png"), position, offset, WAITER_VELOCITY)
		#self._carrying_name: list[Food] = None
		#self._order_list: list[Client, Food] = []

		self.knowledge = Frame("Waiter")
		self.knowledge.set("state", "idle")
		self.knowledge.set("carrying", None)
		self.knowledge.set("orders", [])
    

	def receiveOrder(self, client: Client) -> None:
		#self._order_list.append(client)
		orders = self.knowledge.get("orders")
		orders.append(client)
		self.knowledge.set("orders", orders)
		self.knowledge.set("state","taking order")


	def takeFood(self, cook: Cook) -> None:
		#food_name: str = self._order_list[0].getFoodName()
		#self._carrying_name: str = food_name
		food_name = self.knowledge.get("orders")[0].getFoodName()
		self.knowledge.set("carrying",food_name)
		self.knowledge.set("state","delivering order")
		cook.getAvailableFood()
		# cook.available_counters.insert(0, ) # TODO: make counters available after taking food


	def completeOrder(self) -> None:
		# orders will be completed in a queue approach for now
		#self._order_list[0].receiveFood()
		#self._order_list.pop(0)
		order = self.knowledge.get("orders")
		order[0].receiveFood()
		order.pop(0)
		self.knowledge.set("orders",order)
		self.knowledge.set("state","idle")


	def getOrderList(self) -> list[Client, Food]:
		#return self._order_list
		return self.knowledge.get("orders")
	