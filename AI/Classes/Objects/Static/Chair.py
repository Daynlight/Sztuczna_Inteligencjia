import os
import numpy as np
from enum import Enum

from Classes.Objects.Object import Object
from Classes.Objects.Beings.Client import Client

from conf import PATH_TO_ASSETS

class Orientation(Enum):
	NORTHEAST = 0
	NORTHWEST = 1
	SOUTHEAST = 2
	SOUTHWEST = 3

class Chair(Object):
	def __init__(self, position: np.ndarray[int], render_order: int = 0):
		img: str = "chair01a.png"

		super().__init__(render_order, os.path.join(PATH_TO_ASSETS, "Obstacles", img), position, size=[2, 2])

		self._occupied: bool = False
		self._client: Client | None = None
		self._table = None
    
	def rotate(self,orientation):
		img = "chair01a.png"
		match orientation:
			case "northeast":
				img = "chair01a.png"
			case "northwest":
				img = "chair01b.png"
			case "southeast":
				img = "chair01c.png"
				self.render_order = 2
			case "southwest":
				img = "chair01d.png"
				self.render_order = 2
		self.setTexture(f"Assets/Obstacles/{img}")
		self.setSize([2,2])

	def sitClient(self, client: Client) -> None:
		if not self.getClient():
			self._occupied: bool = True
			self._client: list[Client] = client
    

	def free(self) -> None:
		if self.occupied:
			self._occupied: bool = False
			self._client: list[Client] = None

	
	def getClient(self) -> Client:
		return self._client


	def getTable(self):
		return self._table

	def setTable(self,table):
		self._table=table