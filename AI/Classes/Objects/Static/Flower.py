import numpy as np

from Classes.Core.Object.Object import Object

import Classes.Objects.TextureManager as TextureManager
from Classes.Core.Renderer.Animation.Animation import Animation
from Classes.Core.Renderer.Animation.Frame import Frame

from conf import TILE_SIZE









class Flower(Object):
	def __init__(self, position: np.ndarray[int], render_order: int = 1):
		super().__init__(render_order=render_order, 
									 	 texture=TextureManager.FLOWER1_TEXTURE,
											position=position, size=[2,4], offset=[0, -2 * TILE_SIZE])
		self.setAnimation("Idle", Animation([
			Frame(TextureManager.FLOWER1_TEXTURE, 1),
			Frame(TextureManager.FLOWER2_TEXTURE, 1),
			Frame(TextureManager.FLOWER3_TEXTURE, 1),
			Frame(TextureManager.FLOWER2_TEXTURE, 1)
		]))
		self.setState("Idle")
