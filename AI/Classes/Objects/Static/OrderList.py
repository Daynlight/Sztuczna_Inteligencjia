import numpy as np

from Classes.Core.Object.Object import Object

import Classes.Objects.TextureManager as TextureManager

from conf import TILE_SIZE









class OrderList(Object):
	def __init__(self, position: np.ndarray[int], render_order: int = 1):
		super().__init__(render_order=render_order, 
									 	 texture=TextureManager.ORDER_LIST_TEXTURE,
											position=position, size=[2,2], offset=[TILE_SIZE / 2, -3/2 * TILE_SIZE])
