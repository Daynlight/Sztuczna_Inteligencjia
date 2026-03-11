import os
import numpy as np

from Classes.Objects.Object import Object

from conf import PATH_TO_ASSETS









class Counter(Object):
	def __init__(self, position: np.ndarray[int], render_order: int = 1):
		super().__init__(render_order, os.path.join(PATH_TO_ASSETS, "Obstacles", "counter02_i.png"), position, size=[2,2])
