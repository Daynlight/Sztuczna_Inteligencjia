import numpy as np

from Classes.Core.Object.Object import Object

import Classes.Objects.TextureManager as TextureManager

from conf import TILE_SIZE









class Stove(Object):
	def __init__(self, position: np.ndarray[int], render_order: int = 1):
		super().__init__(render_order=render_order, 
									 	 texture=TextureManager.STOVE_TEXTURE,
											position=position, size=[2,2])
