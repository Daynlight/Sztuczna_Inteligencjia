import os
import numpy as np
from enum import Enum

from Classes.Core.Object.ChairInterface import ChairInterface
from Classes.Core.Renderer.Texture import Texture

from Classes.Objects.Beings.Client import Client
import Classes.Objects.TextureManager as TextureManager


class ChairOrientation(Enum):
	NORTHEAST = 0
	NORTHWEST = 1
	SOUTHEAST = 2
	SOUTHWEST = 3

class Chair(ChairInterface):
	def __init__(self, position: np.ndarray[int], orientation: ChairOrientation = ChairOrientation.NORTHEAST ,render_order = 0):
		texture = TextureManager.CHAIR1_TEXTURE
		super().__init__(position=position, texture=texture, render_order=render_order, size=[2, 2], offset=[0, 0])
		
		self.rotate(orientation)

	
	def rotate(self, orientation):
		texture: Texture = TextureManager.CHAIR1_TEXTURE

		match orientation:
			case ChairOrientation.NORTHEAST:
				texture = TextureManager.CHAIR2_TEXTURE
		
			case ChairOrientation.NORTHWEST:
				texture = TextureManager.CHAIR3_TEXTURE

			case ChairOrientation.SOUTHEAST:
				texture = TextureManager.CHAIR1_TEXTURE
				self._render_order = 2
				
			case ChairOrientation.SOUTHWEST:
				texture = TextureManager.CHAIR4_TEXTURE
				self._render_order = 2
				
		self._texture = texture









'''class Chair(Object):
	def __init__(self, position: np.ndarray[int], orientation: str = "northeast", render_order: int = 0):
		super().__init__(render_order=render_order, 
									   texture=TextureManager.CHAIR1_TEXTURE,
										 position=position, size=[2, 2])

		self._occupied: bool = False
		self._client: Client | None = None
		self._table = None

		self.rotate(orientation)
    

	def rotate(self,orientation):
		texture: Texture = TextureManager.CHAIR1_TEXTURE
		match orientation:
			case "northeast":
				texture: Texture = TextureManager.CHAIR2_TEXTURE
			case "northwest":
				texture: Texture = TextureManager.CHAIR3_TEXTURE
			case "southeast":
				texture: Texture = TextureManager.CHAIR1_TEXTURE
				self.render_order = 2
			case "southwest":
				texture: Texture = TextureManager.CHAIR4_TEXTURE
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
		self._table=table'''