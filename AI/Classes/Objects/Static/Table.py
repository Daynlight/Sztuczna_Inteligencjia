import os
import numpy as np

from Classes.Core.Object.Object import Object
from Classes.Objects.Static.Chair import Chair
from Classes.Objects.Beings.Client import Client

import Classes.Objects.TextureManager as TextureManager


class Table(Object):
    def __init__(self, position: np.ndarray[int], render_order: int = 1):
            super().__init__(render_order = render_order, texture = TextureManager.TABLE_TEXTURE, position = position, size = [2, 2])






'''class Table(Object):
	def __init__(self, position: np.ndarray[int], render_order: int = 1):
		super().__init__(render_order=render_order, 
									 	 texture=TextureManager.TABLE_TEXTURE,
										 position=position, size=[2, 2])
		self._occupied: bool = False

		from Classes.Objects.Static.GroupTable import GroupTable
		
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
		if chair.getTable() is None:
			self._chairs.append(chair)
			chair.setTable(self)
		else:
			print("chair is assigned to other table")


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
		self._group=group'''