import numpy as np
import heapq

from Classes.Core.Object.Object import Object
from Classes.Core.Grid.Grid import Grid_Tile

from Classes.Core.Renderer.Texture import Texture

from conf import GRID_X, GRID_Y









class Being(Object):
  def __init__(self, render_order: int, texture: Texture, position: np.ndarray[int] = [0, 0], 
               offset: np.ndarray[int] = [0, 0], velocity: float = 0, size: np.ndarray[float] = [1, 1]):
    super().__init__(render_order=render_order, texture=texture, position=position, offset=offset, size=size)

    self._velocity: float = velocity
    self._path: np.ndarray[np.ndarray[int]] = []
    self._accTime: float = 0.0


  def goTo(self, hovered_tile : Grid_Tile, collisions: np.ndarray[Object]) -> None:
    target = np.array([hovered_tile.isometric_x, hovered_tile.isometric_y])
    okay: bool = True
    for object in collisions:
      if(np.array_equal(object.getPosition(), target)):
        okay = False
        break
    if(okay):
      self.generatePath(self.getPosition(), hovered_tile, collisions)


  def calculateDistance(self, current_position: np.ndarray[int], position: np.ndarray[int]) -> float:
    return np.linalg.norm(np.array(current_position) - np.array(position))
  

  def generatePath(self, current_position: np.ndarray[int], position: np.ndarray[int], collisions: np.ndarray[Object]) -> None:
    start = np.array(current_position)
    target = np.array([position.isometric_x, position.isometric_y])

    directions = [
      np.array([1, 0]),
      np.array([-1, 0]),
      np.array([0, 1]),
      np.array([0, -1]),
      np.array([1, 1]),
      np.array([1, -1]),
      np.array([-1, 1]),
      np.array([-1, -1])
    ]

    start_key = tuple(start)
    target_key = tuple(target)

    open_set = []
    heapq.heappush(open_set, (0, start_key))
    
    came_from = {}
    g_score = {start_key: 0}

    visited = set()

    while open_set:
      _, current = heapq.heappop(open_set)

      if current == target_key:
        break

      if current in visited:
        continue
      visited.add(current)

      for d in directions:
        neighbor = tuple(np.array(current) + d)

        collision = any(
          np.array_equal(el.getPosition(), np.array(neighbor))
          for el in collisions
        )

        if neighbor[0] < 0 or neighbor[1] < 0 or neighbor[0] > GRID_X or neighbor[1] > GRID_Y:
          collision = True

        if collision:
          continue

        tentative_g = g_score[current] + 1

        if neighbor not in g_score or tentative_g < g_score[neighbor]:
          g_score[neighbor] = tentative_g
          f_score = tentative_g + self.calculateDistance(neighbor, target_key)
          heapq.heappush(open_set, (f_score, neighbor))
          came_from[neighbor] = current

    final_path = []
    temp = target_key
    if temp not in came_from:
      print("No path found!")
      self._path = []
      return

    while temp != start_key:
      final_path.append(np.array(temp))
      temp = came_from[temp]

    self._path = final_path[::-1]


  def makeStep(self, deltaTime: float, acceleration: float) -> None:
    if(len(self._path) <= 0): 
      self.accTime = 0
      return

    self._accTime += deltaTime
    if(self._accTime >= np.linalg.norm(self.getPosition() - self._path[0])/(self._velocity * acceleration)):
      self.setPosition(self._path[0])
      self._path.pop(0)
      self._accTime -= self._accTime
      self.lit_surface = None
