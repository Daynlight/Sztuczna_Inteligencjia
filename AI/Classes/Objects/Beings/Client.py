import random
import numpy as np

from Classes.Core.Object.Being import Being

from Classes.Core.Renderer.Texture import Texture
from Classes.Menu import Menu
from Classes.Objects.Static.Food import Food
import Classes.Objects.TextureManager as TextureManager

from conf import DEBUG









class Client(Being):
	def __init__(self, position: np.ndarray[int], offset: np.ndarray[int] = [0, 0]):
		super().__init__(render_order=3, texture=TextureManager.CLIENT_TEXTURE, 
									   position=position, offset=offset, velocity=2)
		self._table = None
		self._chair = None
		self._wants_to_order: bool = False
		self._waiting_for_food: bool = False
		self._eating: bool = False
		self._food_name: str = None


	def assignTable(self, table) -> None:
		for chair in table.getChairs():
			if not chair.getClient():
				self._table = table
				self._chair = chair
				chair.sitClient(self)
				self.setPosition(chair.getPosition())
				return


	def makeOrder(self, food_name: str) -> None:
		self._wants_to_order = True
		self._food_name = food_name
		if(DEBUG): print(f"Client at {self.getPosition()} wants to order {food_name}")

	def waitForFood(self) -> None:
		self._wants_to_order = False
		self._waiting_for_food = True

	def receiveFood(self) -> None:
		self._waiting_for_food = False
		self._eating = True

	def finishEating(self) -> None:
		self._eating = False
		if(DEBUG): print(f"Client at {self.getPosition()} finished eating {self._food_name}")
		self._food_name = None
	
	def getFoodName(self) -> str:
		return self._food_name

	def decide_order(self, food_list: list[str]) -> None:
		if not self._wants_to_order and not self._waiting_for_food and not self._eating:
			self.makeOrder(random.choice(food_list))
