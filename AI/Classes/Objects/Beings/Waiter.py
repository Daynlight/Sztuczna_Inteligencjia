import os
import numpy as np

from Classes.Core.Object.Being import Being
from Classes.Core.Grid.Grid import Grid

#from Classes.Decision_Tree.ID3 import bool_to_str, build_waiter_decision_tree
from Classes.Neural_Network.network import bool_to_str, WaiterAI
from Classes.Objects.Beings.Client import Client
from Classes.Objects.Beings.Cook import Cook
from Classes.Objects.Static.Food import Food
from Classes.Objects.Static.OrderList import OrderList
import Classes.Objects.TextureManager as TextureManager

from conf import WAITER_VELOCITY, DEBUG









class Waiter(Being):
	def __init__(self, position: np.ndarray[int], offset: np.array = [0, 0]):
		super().__init__(render_order=3, 
									 	 texture=TextureManager.WAITER_TEXTURE,
										 position=position, offset=offset, velocity=WAITER_VELOCITY, size=[1, 2])
		self._carrying: list[Food] = []
		self._order_list: list[Client, Food] = []
		self._order_list_sent: bool = False
		#self._decision_tree = build_waiter_decision_tree()

		self._ai = WaiterAI()
		# jeśli model istnieje → wczytaj
		#if os.path.exists("waiter_model.pth"):
		#	self._ai.load()
		# jeśli model nie istnieje → wytrenuj i zapisz
		#else:
		self._ai.train()


	def receiveOrder(self, client: Client) -> None:
		if abs(self._position[0] - client.getPosition()[0]) + abs(self._position[1] - client.getPosition()[1]) == 1:
			self._order_list.append((client, client.getFoodName()))
			client.waitForFood()
			self._order_list_sent = False
			if(DEBUG): print(f"Waiter received order from client at {client.getPosition()}: {client.getFoodName()}")
			return


	def takeFood(self, cook: Cook) -> None:
		if abs(self._position[0] - cook.getPosition()[0]) + abs(self._position[1] - cook.getPosition()[1]) == 1:
			if cook.hasAvailableFood():
				food = cook.getAvailableFood()
				if food:
					self._carrying.append(food)
					if(DEBUG): print(f"Waiter took {food.getName()} from cook")


	def giveOrderList(self, cook: Cook, order_list: OrderList) -> None:
		if not self._order_list or self._order_list_sent:
			return

		if abs(self._position[0] - order_list.getPosition()[0]) + abs(self._position[1] - order_list.getPosition()[1]) == 1:
			cook.takeOrderFromWaiter(self)
			self._order_list_sent = True
			if(DEBUG): print("Waiter gave order list to cook")


	def completeOrder(self, client: Client) -> bool:
		if abs(self._position[0] - client.getPosition()[0]) + abs(self._position[1] - client.getPosition()[1]) == 1:
			self._order_list.pop(self._order_list.index((client, client.getFoodName())))
			client.receiveFood()
			if(DEBUG): print(f"Client at {client.getPosition()} received their food: {client.getFoodName()}")
			return True
		return False


	def getOrderList(self) -> list[Client, Food]:
		return self._order_list


	def _build_state_features(self, clients, cook: Cook) -> dict[str, str]:
		return {
			"amount_waiting": str(sum(client._waiting_for_food for client in clients)),
			"cook_has_available_food": bool_to_str(cook.hasAvailableFood()),
			"has_carrying_food": bool_to_str(len(self._carrying) > 0),
			"has_pending_orders": bool_to_str(len(self._order_list) > 0),
			"order_list_sent": bool_to_str(self._order_list_sent),
			"any_client_wants_order": bool_to_str(any(client._wants_to_order for client in clients)),
			"any_client_waiting_for_food": bool_to_str(any(client._waiting_for_food for client in clients)),
			"cook_has_pending_orders": bool_to_str(cook.hasPendingOrders()),
		}


	def _deliver_food(self, grid, clients: list[Client]) -> None:
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
			self.goTo(grid, delivery_client.getPosition())
			if self.completeOrder(delivery_client):
				self._carrying.remove(delivery_food)
				delivery_client.finishEating()
		else:
			self._path = []


	def decide(self, grid: Grid, clients, cook: Cook, order_list: OrderList) -> None:
		state = self._build_state_features(clients, cook)
		#action = self._decision_tree.predict(state)
		action = self._ai.predict(state)
		# print(f"Waiter decision: {action}")
		if action == "give_order_list":
			self.goTo(grid, order_list.getPosition())
			self.giveOrderList(cook, order_list)
			return

		if action == "take_food":
			self.goTo(grid, cook.getPosition())
			self.takeFood(cook)
			return

		if action == "deliver_food":
			self._deliver_food(grid, clients)
			return

		if action == "take_order":
			for client in clients:
				if client._wants_to_order:
					self.goTo(grid, client.getPosition())
					self.receiveOrder(client)
					return

		# Fallback to original rule-based behavior when the tree cannot decide.
		all_waiting = len(clients) > 0 and all(client._waiting_for_food for client in clients)

		if all_waiting and len(self.getOrderList()) > 0 and not self._order_list_sent:
			self.goTo(grid, order_list.getPosition())
			self.giveOrderList(cook, order_list)
			return

		if cook.hasAvailableFood():
			self.goTo(grid, cook.getPosition())
			self.takeFood(cook)
			return

		if self._carrying:
			self._deliver_food(grid, clients)
			return

		for client in clients:
			if client._wants_to_order:
				self.goTo(grid, client.getPosition())
				self.receiveOrder(client)
				return
	
