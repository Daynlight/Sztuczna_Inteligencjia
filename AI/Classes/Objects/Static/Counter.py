import os
import numpy as np

from Classes.Core.Object.Object import Object

from Classes.Core.Renderer.Texture import Texture

from conf import PATH_TO_ASSETS









class Counter(Object):
	def __init__(self, position: np.ndarray[int], render_order: int = 1):
		super().__init__(render_order=render_order, 
									 	 texture=Texture(texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Counter", "Counter.png"), 
									   								 normal_texture_path=os.path.join(PATH_TO_ASSETS, "Handmade", "Static", "Counter", "Counter_Normals.png"),
																		 size=[2, 2]), 
											position=position, size=[2,2])
