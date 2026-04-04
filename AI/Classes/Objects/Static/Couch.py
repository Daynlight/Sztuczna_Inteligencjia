import os
import numpy as np
from enum import Enum

from Classes.Core.Object.Object import Object
from Classes.Core.Renderer.Texture import Texture

from Classes.Objects.Beings.Client import Client
import Classes.Objects.TextureManager as TextureManager

from conf import TILE_SIZE

class Orientation(Enum):
	NORTHEAST = 0
	NORTHWEST = 1
	SOUTHEAST = 2
	SOUTHWEST = 3





class Couch(Object):
	def __init__(self, position: np.ndarray[int], orientation: str = "northeast", render_order: int = 0):
		super().__init__(render_order=render_order, 
									   texture=TextureManager.COUCH1_TEXTURE,
										 position=position, size=[2, 4], offset=[-TILE_SIZE, -2.5*TILE_SIZE])

		self._occupied: bool = False
		self._client: Client | None = None
		self._table = None

		self.rotate(orientation)
    

	def rotate(self,orientation):
		texture: Texture = TextureManager.COUCH1_TEXTURE
		match orientation:
			case "northeast":
				texture: Texture = TextureManager.COUCH2_TEXTURE
			case "northwest":
				texture: Texture = TextureManager.COUCH3_TEXTURE
			case "southeast":
				texture: Texture = TextureManager.COUCH1_TEXTURE
				self.render_order = 2
			case "southwest":
				texture: Texture = TextureManager.COUCH4_TEXTURE
				self.render_order = 2

		self._texture = texture


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