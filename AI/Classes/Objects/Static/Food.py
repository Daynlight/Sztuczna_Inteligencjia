import os
import numpy as np

from Classes.Core.Object.Object import Object

from Classes.Core.Renderer.Texture import Texture

from conf import PATH_TO_ASSETS









class Food(Object):
	def __init__(self, name: str, position: np.ndarray[int]):
		super().__init__(render_order=3, texture=Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Food", f"{name}_dish.png")), position=position)
