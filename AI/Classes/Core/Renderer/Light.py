import numpy as np


class Light:
  def __init__(self, position: np.ndarray[int], color: np.ndarray[float], strength: float):
    self.position = position
    self.color = color
    self.strength = strength
