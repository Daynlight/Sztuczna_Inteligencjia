import os
import numpy as np

from Classes.Objects.Object import Object
from Classes.Objects.Static.Chair import Chair
from Classes.Objects.Beings.Client import Client

from conf import PATH_TO_ASSETS









class Table(Object):
	def __init__(self, position: np.ndarray[int], render_order: int = 1):
		super().__init__(render_order, os.path.join(PATH_TO_ASSETS, "Obstacles", "table05a.png"), position, size = [2,2])
		self._occupied: bool = False
		
		self._chairs: list[Chair] = list([])
		self._clients: list[Client] = list([])


	def seatClient(self, client: np.ndarray[Client]) -> None:
		self._clients: np.ndarray[Client] = client
		self._occupied = True


	def free(self) -> None:
		self._clients: list[Client] = list([], dtype=Client)
		self._occupied = False


	def addChair(self, chair: Chair) -> None:
		self._chairs.append(chair)


	def removeChair(self, chair: Chair) -> None:
		if chair in self._chairs:
			self._chairs.remove(chair)

	
	def getChairs(self) -> list[Chair]:
		return self._chairs
	

	def getClients(self) -> list[Client]:
		return self._clients
