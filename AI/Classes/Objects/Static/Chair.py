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
	def __init__(self, position: np.ndarray[int], orientation: Orientation, render_order: int = 0):
		img: str = "chair01a.png"
		match orientation:
			case Orientation.NORTHEAST:
				img: str = "chair01a.png"
			case Orientation.NORTHWEST:
				img: str = "chair01b.png"
			case Orientation.SOUTHEAST:
				img: str = "chair01c.png"
				render_order: int = 2
			case Orientation.SOUTHWEST:
				img: str = "chair01d.png"
				render_order: int = 2

		super().__init__(render_order, os.path.join(PATH_TO_ASSETS, "Obstacles", img), position, size=[2, 2])

		self._occupied: bool = False
		self._client: list[Client] = None
    

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
