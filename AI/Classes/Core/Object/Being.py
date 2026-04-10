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
    self._path: list = []
    self._accTime: float = 0.0
    self._rotation: int = 0
    

  def goTo(self, goal, collisions: np.ndarray[Object], walls: np.ndarray[Wall]) -> None:
    target = self._resolve_goal_target(goal, collisions)
    if target is None:
      return

    collisions_filtered = np.array([c for c in collisions if c is not self], dtype=object)
    if self._is_collision(target, collisions_filtered):
      return

    self.generatePath(self.getPosition(), target, collisions_filtered, walls)


  def _resolve_goal_target(self, goal, collisions: np.ndarray[Object]) -> np.ndarray[int] | None:
    if hasattr(goal, "isometric_x") and hasattr(goal, "isometric_y"):
      return np.array([goal.isometric_x, goal.isometric_y])

    if hasattr(goal, "getPosition"):
      goal_pos = np.array(goal.getPosition())
      if hasattr(goal, "getClient") and goal.getClient():
        adjacent = self._find_adjacent_target(goal_pos, collisions)
        return adjacent if adjacent is not None else goal_pos

      if self._is_collision(goal_pos, collisions):
        adjacent = self._find_adjacent_target(goal_pos, collisions)
        return adjacent if adjacent is not None else goal_pos

      return goal_pos

    return None


  def _find_adjacent_target(self, position: np.ndarray[int], collisions: np.ndarray[Object]) -> np.ndarray[int] | None:
    directions = [
      np.array([0, -1]),
      np.array([1, 0]),
      np.array([0, 1]),
      np.array([-1, 0])
    ]

    best_target = None
    best_distance = float("inf")
    current_position = self.getPosition()

    for direction in directions:
      candidate = position + direction
      if candidate[0] < 0 or candidate[1] < 0 or candidate[0] >= GRID_X or candidate[1] >= GRID_Y:
        continue

      if self._is_collision(candidate, collisions):
        continue

      distance = self.calculateDistance(current_position, candidate)
      if distance < best_distance:
        best_distance = distance
        best_target = candidate

    return best_target


  def _is_collision(self, target: np.ndarray[int], collisions: np.ndarray[Object]) -> bool:
    return any(np.array_equal(el.getPosition(), target) for el in collisions)


  def rotate(self, direction: str) -> None:
    direction_mapping = {
      "left": -1,
      "right": 1
    }
    self._rotation = (self._rotation + direction_mapping[direction]) % 4
    print(f"Being rotated {direction}")

    
  def calculateDistance(self, current_position: np.ndarray[int], position: np.ndarray[int]) -> float:
    return np.linalg.norm(np.array(current_position) - np.array(position))
  

  def generatePath(self, current_position: np.ndarray[int], position, collisions: np.ndarray[Object], walls: np.ndarray[Wall]) -> None:
    start = np.array(current_position)
    start_r = self._rotation

    if hasattr(position, "isometric_x") and hasattr(position, "isometric_y"):
      target = np.array([position.isometric_x, position.isometric_y])
    elif isinstance(position, np.ndarray):
      target = np.array(position)
    elif hasattr(position, "getPosition"):
      target = np.array(position.getPosition())
    else:
      target = np.array(position)

    # possible movements from current position
    directions = [
      np.array([0, -1]),  # 0 north
      np.array([1, 0]),   # 1 east
      np.array([0, 1]),   # 2 south
      np.array([-1, 0])   # 3 west
    ]

    start_key = (tuple(start), start_r)
    target_pos = tuple(target)

    open_set = []
    heapq.heappush(open_set, (0, start_key))
    came_from = {}
    g_score = {start_key: 0}
    visited = set()
    rotate_cost = 0.1
    move_cost = 1
    
    while open_set:
      # getting tile to check
      _, current = heapq.heappop(open_set)
      current_pos, current_r = current

      if tuple(current_pos) == target_pos:
        break

      if current in visited:
        continue
      
      # adding current to visited list
      visited.add(current)

      # move forward
      d = directions[current_r]
      neighbor_pos = np.array(current_pos) + d
      if neighbor_pos[0] >= 0 and neighbor_pos[1] >= 0 and neighbor_pos[0] < GRID_X and neighbor_pos[1] < GRID_Y:
        collision = any(np.array_equal(el.getPosition(), neighbor_pos) for el in collisions)
        
        if not collision:
          for el in walls:
            # getting two lists of restricted movement (going through wall)
            restricted_movement = el.getMovementRestriction()
            if restricted_movement is None:
              continue
            
            # first check
            in_restricted_area = False
            for el in restricted_movement[0]:
              if np.array_equal(el, current_pos):
                in_restricted_area = True
                break
              
            if in_restricted_area:
              for el in restricted_movement[1]:
                if np.array_equal(el, neighbor_pos):
                  collision = True
                  break
            
            # second check (opposite direction)
            in_restricted_area = False
            for el in restricted_movement[1]:
              if np.array_equal(el, current_pos):
                in_restricted_area = True
                break
              
            if in_restricted_area:
              for el in restricted_movement[0]:
                if np.array_equal(el, neighbor_pos):
                  collision = True
                  break

        if not collision:
          neighbor_key = (tuple(neighbor_pos), current_r)
          tentative_g = g_score[current] + move_cost
          if neighbor_key not in g_score or tentative_g < g_score[neighbor_key]:
            g_score[neighbor_key] = tentative_g
            f_score = tentative_g + self.calculateDistance(neighbor_pos, target)
            heapq.heappush(open_set, (f_score, neighbor_key))
            came_from[neighbor_key] = current

      # rotate left
      new_r = (current_r - 1) % 4
      neighbor_key = (current_pos, new_r)
      tentative_g = g_score[current] + rotate_cost
      if neighbor_key not in g_score or tentative_g < g_score[neighbor_key]:
        g_score[neighbor_key] = tentative_g
        f_score = tentative_g + self.calculateDistance(current_pos, target)
        heapq.heappush(open_set, (f_score, neighbor_key))
        came_from[neighbor_key] = current

      # rotate right
      new_r = (current_r + 1) % 4
      neighbor_key = (current_pos, new_r)
      tentative_g = g_score[current] + rotate_cost
      if neighbor_key not in g_score or tentative_g < g_score[neighbor_key]:
        g_score[neighbor_key] = tentative_g
        f_score = tentative_g + self.calculateDistance(current_pos, target)
        heapq.heappush(open_set, (f_score, neighbor_key))
        came_from[neighbor_key] = current

    final_path = []
    temp = None
    for key in came_from.keys():
      if tuple(key[0]) == target_pos:
        temp = key
        break
    if temp is None:
      print("No path found!")
      self._path = []
      return

    # move through came_from to start
    while temp != start_key:
      final_path.append(temp)
      temp = came_from[temp]

    # reverse path
    self._path = final_path[::-1]


  def makeStep(self, deltaTime: float, acceleration: float) -> None:
    if len(self._path) <= 0: 
      self._accTime = 0
      return

    next_pos, next_r = self._path[0]
    next_pos_arr = np.array(next_pos)
    current_pos_arr = np.array(self.getPosition())

    if np.array_equal(next_pos_arr, current_pos_arr):
      # rotate
      print(f"New rotation: {"north" if next_r == 0 else "east" if next_r == 1 else "south" if next_r == 2 else "west"}")
      self._rotation = next_r
      self._path.pop(0)
    else:
      # move
      self._accTime += deltaTime
      dist = np.linalg.norm(current_pos_arr - next_pos_arr)
      if self._accTime >= dist / (self._velocity * acceleration):
        self.setPosition(next_pos_arr.tolist())
        self._rotation = next_r
        self._path.pop(0)
        self._accTime = 0
        self.lit_surface = None
