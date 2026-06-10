import pygame
import numpy as np

from Classes.Core.Renderer.Texture import Texture
from Classes.Core.Renderer.Light import Light









class Frame:
  def __init__(self, texture: Texture, time: float):
    self._texture: Texture = texture
    self._time: float = time
    self._last_pos: np.ndarray[int] = None
    self._lit_texture: pygame.Surface = None


  def getTexture(self, render_pos: np.ndarray[int], lights: np.ndarray[Light]):
    if(self._lit_texture is None or self._last_pos is None or not np.array_equal(self._last_pos, render_pos)):
      self._lit_texture: pygame.Surface = self._texture.getLitTexture(render_pos, lights).copy()
    self._last_pos = render_pos.copy()

    return self._lit_texture

  def getTime(self) -> float:
    return self._time



