import os
import numpy as np
import pygame
from concurrent.futures import ThreadPoolExecutor, as_completed

from Classes.Core.Object.Object import Object
from Classes.Core.Renderer.Texture import Texture
from Classes.Core.Renderer.Light import Light
from Classes.Core.Grid.Grid import Grid
from Classes.Core.Renderer.Renderer import Renderer

from conf import TILE_SIZE









# [NOTE] use direction as [0, 1] or [1, 0] nothing else this will break path finding
class Wall():
  def __init__(self, texture: Texture, position: np.ndarray[int] = [0, 0], direction: np.ndarray[int] = [0, 0], numbers: int = 1):
    self._walls = []

    for i in range(numbers):
      new_pos: np.ndarray[int] = np.array(position, dtype=int) + np.array(direction, dtype=int) * i
      object = Object(render_order=-1, 
                      texture=texture,
                      position=new_pos, offset=[0, -2 * TILE_SIZE], size=[2, 4])
      self._walls.append(object)

    self._walls = np.array(self._walls, dtype=Object)
    self._direction = direction
    self._position = position
    self._numbers = numbers
    self._restricted_movement = []
    self._restricted_movement_initialized = False
      

  def precomputeLight(self, grid: "Grid", lights: list):
    tasks = []

    with ThreadPoolExecutor() as executor:
      for el in self._walls:
        tasks.append(executor.submit(el.precomputeLight, grid, lights))
      for future in as_completed(tasks):
        future.result()


  def render(self, surface: pygame.Surface, grid: Grid, renderer: Renderer, lights: np.ndarray[Light]):
    for el in self._walls:
      el.render(surface, grid, renderer, lights)


  def getMovementRestriction(self):
    if(self._restricted_movement_initialized == True): return self._restricted_movement
    
    parallel_vector = np.array(self._direction @ np.array([[0, -1], [1, 0]]))
    vector_norm = np.linalg.norm(parallel_vector)
    if(vector_norm != 0): parallel_vector = parallel_vector * (1 / vector_norm)

    # change direction for generation on outside
    if(parallel_vector[1] < 0): parallel_vector = -1 * parallel_vector
    
    tile_a_restriction = []
    tile_b_restriction = []
    for i in range(self._numbers):
      new_pos: np.ndarray[int] = np.array(self._position, dtype=int) + np.array(self._direction, dtype=int) * i
      tile_a = new_pos
      tile_b = new_pos - np.array(parallel_vector)
      tile_a_restriction.append(tile_a)
      tile_b_restriction.append(tile_b)

    # additional for fixing wall snapping
    new_pos: np.ndarray[int] = np.array(self._position, dtype=int) - np.array(self._direction, dtype=int)
    tile_a_restriction.append(new_pos)
    new_pos: np.ndarray[int] = np.array(self._position, dtype=int) + np.array(self._direction, dtype=int) * self._numbers
    tile_a_restriction.append(new_pos)

    self._restricted_movement = [tile_a_restriction, tile_b_restriction]
    self._restricted_movement_initialized = True

    return self._restricted_movement


  def getObjects(self) -> np.ndarray[Object]:
    return self._walls

