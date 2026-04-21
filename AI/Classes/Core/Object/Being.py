import numpy as np
import heapq

from Classes.Core.Object.Object import Object
from Classes.Core.Object.Wall import Wall

from Classes.Core.Renderer.Texture import Texture

from conf import GRID_X, GRID_Y, BEING_MOVEMENT_DIRECTIONS, DEBUG, BEING_DEFAULT_ROTATE_COST









class Being(Object):
  def __init__(self, render_order: int, texture: Texture, position: np.ndarray[int] = [0, 0], 
               offset: np.ndarray[int] = [0, 0], velocity: float = 0, size: np.ndarray[float] = [1, 1]):
    super().__init__(render_order=render_order, texture=texture, position=position, offset=offset, size=size)

    self._velocity: float = velocity
    self._path: list = []
    self._accTime: float = 0.0
    self._rotation: int = 0
    

  def goTo(self, grid, goal) -> None:
    if goal is None: 
      return
    
    target = self._find_adjacent_target(grid, goal)
    self.generatePath(grid, self.getPosition(), target)


  def rotate(self, direction: str) -> None:
    direction_mapping = {
      "left": -1,
      "right": 1
    }
    
    self._rotation = (self._rotation + direction_mapping[direction]) % 4
    if(DEBUG): print(f"Being rotated {direction}")

    
  def calculateDistance(self, current_position: np.ndarray[int], position: np.ndarray[int]) -> float:
    return np.linalg.norm(np.array(current_position) - np.array(position))
  

  def _find_adjacent_target(self, grid, position: np.ndarray[int]) -> np.ndarray[int] | None:
    best_target = None
    best_distance = float("inf")
    current_position = self.getPosition()
    list_of_possible_movement = grid.getNeighbors(position)

    for direction in BEING_MOVEMENT_DIRECTIONS:
      candidate = position + direction
      if candidate[0] < 0 or candidate[1] < 0 or candidate[0] >= GRID_X or candidate[1] >= GRID_Y:
        continue
      
      if(tuple(candidate) not in list_of_possible_movement):
        continue

      distance = self.calculateDistance(current_position, candidate)
      if distance < best_distance:
        best_distance = distance
        best_target = candidate

    return best_target


  def updateKey(self, grid, current, target, neighbor_key, cost, g_score, open_set, came_from):
    # calculate new g_score previous + cost cost of tile
    new_g_score = g_score[current] + cost

    # checking if state is already in g_score register and if new one is better then previous
    if neighbor_key not in g_score or new_g_score < g_score[neighbor_key]:
      g_score[neighbor_key] = new_g_score                                      # adding/updating to lowest g_score for state
      f_score = new_g_score + self.calculateDistance(neighbor_key[0], target)  # calculating f_score = g_score + heuristic
      heapq.heappush(open_set, (f_score, neighbor_key))                        # adding to priority queue base on f_score = g_score + heuristic 
      came_from[neighbor_key] = current                                        # adding to graph


  def generatePath(self, grid, current_position: np.ndarray[int], target) -> None:
    if(target is None): return
    
    # start
    start = np.array(current_position)
    start_r = self._rotation
    start_key = (tuple(start), start_r)

    # target
    target_pos = tuple(target)
    goal_node = None

    # priority queue for A*
    open_set = []
    heapq.heappush(open_set, (0, start_key))
    g_score = {start_key: 0}
    visited = set()

    # graph
    came_from = {}
    
    while open_set:
      # getting tile from priority queue
      _, current = heapq.heappop(open_set)
      current_pos, current_r = current

      # checking if we reach target
      if tuple(current_pos) == target_pos:
        goal_node = current
        break

      # checking if we already check this state
      if current in visited:
        continue
      
      # adding current to visited list
      visited.add(current)

      # get neighbors from precomputed grid
      list_of_possible_movement = grid.getNeighbors(current_pos)

      # getting neighbor position when we go forward
      d = BEING_MOVEMENT_DIRECTIONS[current_r]
      neighbor_pos = np.array(current_pos, dtype=int) + d

      # check if forward neighbor is in possible movements precomputed in grid
      if tuple(neighbor_pos) in list_of_possible_movement:
        # generate new key
        neighbor_key = (tuple(neighbor_pos), current_r)
        
        # update key
        cost = grid.getCost(neighbor_key[0])
        self.updateKey(grid, current, target, neighbor_key, cost, g_score, open_set, came_from)

      # generate new key for left rotation
      new_r = (current_r - 1) % 4
      neighbor_key = (current_pos, new_r)
      # update key
      self.updateKey(grid, current, target, neighbor_key, BEING_DEFAULT_ROTATE_COST, g_score, open_set, came_from)

      # generate new key for right rotation
      new_r = (current_r + 1) % 4
      neighbor_key = (current_pos, new_r)
      # update key
      self.updateKey(grid, current, target, neighbor_key, BEING_DEFAULT_ROTATE_COST, g_score, open_set, came_from)


    if goal_node is None:
      if(DEBUG): print("No path found!")
      self._path = []
      return
    
    final_path = []
    temp = goal_node

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
      if(DEBUG): print(f"New rotation: {"north" if next_r == 0 else "east" if next_r == 1 else "south" if next_r == 2 else "west"}")
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
