import os
import numpy as np

from Classes.Objects.Object import Object
from Classes.Objects.Static.Chair import Chair
from Classes.Objects.Beings.Client import Client

from conf import PATH_TO_ASSETS

class Table(Object):
	def __init__(self, position: np.ndarray[int], render_order: int = 1):

		from Classes.Objects.Static.GroupTable import GroupTable

		super().__init__(render_order, os.path.join(PATH_TO_ASSETS, "Obstacles", "table05a.png"), position, size = [2,2])
		self._occupied: bool = False
		
		self._chairs: list[Chair] = list([])
		self._clients: list[Client] = list([])
		self._group: list[GroupTable] = None


	def seatClient(self, client: np.ndarray[Client]) -> None:
		self._clients: np.ndarray[Client] = client
		self._occupied = True


	def free(self) -> None:
		self._clients: list[Client] = list([], dtype=Client)
		self._occupied = False


	def addChair(self, chair: Chair) -> None:
		if chair.getTable is None:
			self._chairs.append(chair)
			chair.setTable(self)
			if chair.getPosition()[0] == self._position[0]+1 and chair.getPosition()[1] == self._position[1]:
				chair.rotate("southeast")
			
			elif chair.getPosition()[0] == self._position[0]-1 and chair.getPosition()[1] == self._position[1]:
				chair.rotate("northwest")
					
			elif chair.getPosition()[0] == self._position[0] and chair.getPosition()[1] == self._position[1]+1:
				chair.rotate("southwest")
					
			elif chair.getPosition()[0] == self._position[0] and chair.getPosition()[1] == self._position[1]-1:
				chair.rotate("northeast")


	def removeChair(self, chair: Chair) -> None:
		if chair in self._chairs:
			self._chairs.remove(chair)
			chair.setTable(None)

	
	def getChairs(self) -> list[Chair]:
		return self._chairs


	def getClients(self) -> list[Client]:
		return self._clients
	
 
	def getGroup(self):
		return self._group

	def setGroup(self,group):
		self._group=group