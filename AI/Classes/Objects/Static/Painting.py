import os
import numpy as np

from Classes.Core.Object.Object import Object

import Classes.Objects.TextureManager as TextureManager

from conf import TILE_SIZE


class Painting(Object):
	def __init__(self, position: np.ndarray[int], render_order: int = 1):
		super().__init__(render_order=render_order, 
									 	 texture=TextureManager.PAINTING_TEXTURE,
											position=position,  offset=[0, -2 * TILE_SIZE] ,size=[2,4])