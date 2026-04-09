import os
import numpy as np

from Classes.Core.Object.Being import Being

from Classes.Core.Renderer.Texture import Texture

from conf import PATH_TO_ASSETS









class Client(Being):
	def __init__(self, position: np.ndarray[int], offset: np.ndarray[int] = [0, 0]):
		super().__init__(render_order=3, texture=Texture(os.path.join(PATH_TO_ASSETS, "Other", "client.png")), 
									   position=position, offset=offset, velocity=2)
		self._table = None
		self._chair = None
		self._waiting: bool = False
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
		self._waiting = True
		self._food_name = food_name


	def receiveFood(self) -> None:
		self._waiting = False
		self._eating = True


	def getFoodName(self) -> str:
		return self._food_name
