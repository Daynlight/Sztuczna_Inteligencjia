import os
import numpy as np

from Classes.Objects.Object import Object

from conf import PATH_TO_ASSETS









class Food(Object):
	def __init__(self, name: str, position: np.ndarray[int]):
		super().__init__(3, os.path.join(PATH_TO_ASSETS, "Food", f"{name}_dish.png"), position)
