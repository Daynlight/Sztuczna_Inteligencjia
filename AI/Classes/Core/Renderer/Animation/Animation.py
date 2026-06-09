import pygame
import numpy as np

from Classes.Core.Renderer.Light import Light
from Classes.Core.Renderer.Animation.Frame import Frame









class Animation:
  def __init__(self, frames: list[Frame]):
    self._frames: list[Frame] = frames
    self._accTime = 0
    self._frame = 0


  def getTexture(self, render_pos: np.ndarray[int], lights: np.ndarray[Light], deltaTime: float) -> pygame.Surface:
    self._accTime += deltaTime

    if(self._accTime >= 1):
      self._frame = (self._frame + 1) % len(self._frames)
      self._accTime = 0

    return self._frames[self._frame].getTexture(render_pos, lights)