import numpy as np
import heapq

from Classes.Core.Object.Object import Object
from Classes.Core.Grid.Grid import Grid_Tile
from Classes.Core.Object.Wall import Wall

from Classes.Core.Renderer.Texture import Texture

from conf import GRID_X, GRID_Y









class Being(Object):
  def __init__(self, render_order: int, texture: Texture, position: np.ndarray[int] = [0, 0], 
               offset: np.ndarray[int] = [0, 0], velocity: float = 0, size: np.ndarray[float] = [1, 1]):
    super().__init__(render_order=render_order, texture=texture, position=position, offset=offset, size=size)

    self._velocity: float = velocity
    self._path: np.ndarray[np.ndarray[int]] = []
    self._accTime: float = 0.0


  def goTo(self, hovered_tile : Grid_Tile, collisions: np.ndarray[Object], walls: np.ndarray[Wall]) -> None:
    target = np.array([hovered_tile.isometric_x, hovered_tile.isometric_y])
    okay: bool = True
    for object in collisions:
      if(np.array_equal(object.getPosition(), target)):
        okay = False
        break
    if(okay):
      self.generatePath(self.getPosition(), hovered_tile, collisions, walls)


  def calculateDistance(self, current_position: np.ndarray[int], position: np.ndarray[int]) -> float:
    return np.linalg.norm(np.array(current_position) - np.array(position))
  

  def generatePath(self, current_position: np.ndarray[int], position: np.ndarray[int], collisions: np.ndarray[Object], walls: np.ndarray[Wall]) -> None:
    start = np.array(current_position)
    target = np.array([position.isometric_x, position.isometric_y])

    # possible movements from current position
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
      # getting tile to check
      _, current = heapq.heappop(open_set)

      # checking tile
      if current == target_key:
        break

      if current in visited:
        continue
      
      # adding current to visited list
      visited.add(current)

      # checking neighbors
      for d in directions:
        # getting neighbor
        neighbor = tuple(np.array(current) + d)

        # checking collisions with objects
        collision = any(
          np.array_equal(el.getPosition(), np.array(neighbor))
          for el in collisions
        )

        # checking map edges
        if neighbor[0] < 0 or neighbor[1] < 0 or neighbor[0] >= GRID_X or neighbor[1] >= GRID_Y:
          collision = True
        
        # checking walls
        if(collision == False):
          for el in walls:
            # getting two lists of restricted movement (going through wall)
            restricted_movement = el.getMovementRestriction()
            if(restricted_movement == None): continue
            
            # first check
            in_restricted_area = False
            for el in restricted_movement[0]:
              if(np.array_equal(el, current)):
                in_restricted_area = True
                break
              
            if(in_restricted_area == True):
              for el in restricted_movement[1]:
                if(np.array_equal(el, neighbor)):
                  collision = True
                  break
            
            # second check (opposite direction)
            in_restricted_area = False
            for el in restricted_movement[1]:
              if(np.array_equal(el, current)):
                in_restricted_area = True
                break
              
            if(in_restricted_area == True):
              for el in restricted_movement[0]:
                if(np.array_equal(el, neighbor)):
                  collision = True
                  break
        
        # if collision than we skip this node
        if collision:
          continue

        # calculate score distance from start
        tentative_g = g_score[current] + 1

        # adding neighbor for future check
        if neighbor not in g_score or tentative_g < g_score[neighbor]:
          g_score[neighbor] = tentative_g
          f_score = tentative_g + self.calculateDistance(neighbor, target_key)
          heapq.heappush(open_set, (f_score, neighbor))
          came_from[neighbor] = current

    final_path = []
    temp = target_key
    # check if we found path
    if temp not in came_from:
      print("No path found!")
      self._path = []
      return

    # move through came_from to start
    while temp != start_key:
      final_path.append(np.array(temp))
      temp = came_from[temp]

    # reverse path
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
