import os
import numpy as np
from enum import Enum

from Classes.Core.Object.Object import Object
from Classes.Objects.Beings.Client import Client

from Classes.Core.Renderer.Texture import Texture

from conf import PATH_TO_ASSETS









class Orientation(Enum):
	NORTHEAST = 0
	NORTHWEST = 1
	SOUTHEAST = 2
	SOUTHWEST = 3









class Chair(Object):
	def __init__(self, position: np.ndarray[int], orientation: str = "northeast", render_order: int = 0):
		img: str = "Chair1.png"
		super().__init__(render_order=render_order, 
									   texture=Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Chair", img),
																		 size=[2, 2]), 
										 position=position, size=[2, 2])

		self._occupied: bool = False
		self._client: Client | None = None
		self._table = None

		self.rotate(orientation)
    

	def rotate(self,orientation):
		img = "Chair1.png"
		img_norm = ""
		match orientation:
			case "northeast":
				img = "Chair2.png"
				img_norm = "Chair2_Normals.png"
			case "northwest":
				img = "Chair3.png"
				img_norm = "Chair3_Normals.png"
			case "southeast":
				img = "Chair1.png"
				img_norm = "Chair1_Normals.png"
				self.render_order = 2
			case "southwest":
				img = "Chair4.png"
				img_norm = "Chair4_Normals.png"
				self.render_order = 2

		self._texture.setTexture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Chair", img), 
													   normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Chair", img_norm))
		self._texture.setSize([2,2])


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