import os
import numpy as np
import pygame

from Classes.Core.Object.Object import Object
from Classes.Core.Renderer.Texture import Texture
from Classes.Core.Renderer.Light import Light
from Classes.Core.Grid.Grid import Grid
from Classes.Core.Renderer.Renderer import Renderer

from conf import PATH_TO_ASSETS, TILE_SIZE









class WallObject():
  def __init__(self, texture_path: str, normals_texture_path: str = "", position: np.ndarray[int] = [0, 0], direction: np.ndarray[int] = [0, 0], numbers: int = 1):
    self._walls = []

    for i in range(numbers):
      new_pos: np.ndarray[int] = np.array(position, dtype=int) + np.array(direction, dtype=int) * i
      object = Object(render_order=-1, 
                      texture=Texture(texture_path=os.path.join(PATH_TO_ASSETS, texture_path), 
                                      normal_texture_path=os.path.join(PATH_TO_ASSETS, normals_texture_path),
                                      size=[2, 4]),
                      position=new_pos, offset=[0, -2 * TILE_SIZE], size=[2, 4])
      self._walls.append(object)

    self._walls = np.array(self._walls, dtype=Object)
      

  def precomputeLight(self, grid: Grid, lights: np.ndarray[Light]):
    for el in self._walls:
      el.precomputeLight(grid, lights)


  def render(self, surface: pygame.Surface, grid: Grid, renderer: Renderer, lights: np.ndarray[Light]):
    for el in self._walls:
      el.render(surface, grid, renderer, lights)
