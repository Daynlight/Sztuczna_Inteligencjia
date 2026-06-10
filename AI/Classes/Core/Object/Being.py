import numpy as np
import heapq
from collections import deque
import pygame

from Classes.Core.Object.Object import Object
from Classes.Core.Object.Wall import Wall

from Classes.Core.Renderer.Texture import Texture

from conf import GRID_X, GRID_Y, TILE_SIZE, BEING_MOVEMENT_DIRECTIONS, DEBUG, BEING_DEFAULT_ROTATE_COST, PATH_SEARCH_VARIANTS, PATH_SEARCH_VARIANT, SEARCH_VISUALIZATION
from Classes.Objects.TextureManager import TO_CHECK_TEXTURE, EXPLORED_TEXTURE, CORRECT_TEXTURE









class Being(Object):
  def __init__(self, render_order: int, texture: Texture, position: np.ndarray[int] = [0, 0], 
               offset: np.ndarray[int] = [0, 0], velocity: float = 0, size: np.ndarray[float] = [1, 1]):
    super().__init__(render_order=render_order, texture=texture, position=position, offset=offset, size=size)

    self._velocity: float = velocity
    self._path: list = []
    self._accTime: float = 0.0
    self._rotation: int = 0
    self._visualize: dict[tuple, Object] = {}

    self._open_set = []
    self._start_key = tuple()
    self._searching_for_path = False
  

  def pathIsEmpty(self):
    return len(self._path) == 0
  

  def searchingForPath(self):
    return self._searching_for_path


  def rotate(self, direction: str) -> None:
    direction_mapping = {
      "left": -1,
      "right": 1
    }
    
    self._rotation = (self._rotation + direction_mapping[direction]) % 4
    if(DEBUG): print(f"Being rotated {direction}")

    
  def calculateDistance(self, current_position: np.ndarray[int], position: np.ndarray[int]) -> float:
    return abs(current_position[0] - position[0]) + abs(current_position[1] - position[1])
  

  def _find_adjacent_target(self, grid, position: np.ndarray[int]) -> np.ndarray[int] | None:
    best_target = None
    best_distance = float("inf")
    current_position = tuple(self.getPosition())

    pos_tuple = tuple(position)
    list_of_possible_movement = grid.getNeighbors(position)

    for direction in BEING_MOVEMENT_DIRECTIONS:
      candidate = (pos_tuple[0] + int(direction[0]), pos_tuple[1] + int(direction[1]))

      if candidate[0] < 0 or candidate[1] < 0 or candidate[0] >= GRID_X or candidate[1] >= GRID_Y:
        continue
      
      if(candidate not in list_of_possible_movement):
        continue

      distance = self.calculateDistance(current_position, candidate)
      if distance < best_distance:
        best_distance = distance
        best_target = np.array(candidate)

    return best_target


  def goTo(self, grid, goal) -> None:
    if goal is None: 
      return
    
    self._visualize = {}
    
    self._target = self._find_adjacent_target(grid, goal)

    match PATH_SEARCH_VARIANT:
      case PATH_SEARCH_VARIANTS.A_STAR:
        self.prepareAStar(self.getPosition())
      case PATH_SEARCH_VARIANTS.BFS:
        self.prepareBFS(self.getPosition())
      case _:
        self.prepareAStar(self.getPosition())


  def calculatePath(self, iterations, grid, renderer, lights):
    for _ in range(iterations):
      if(self._searching_for_path == False): return
      match PATH_SEARCH_VARIANT:
        case PATH_SEARCH_VARIANTS.A_STAR:
          self.stepAStar(grid, renderer, lights)
        case PATH_SEARCH_VARIANTS.BFS:
          self.stepBFS(grid, renderer, lights)
        case _:
          self.stepAStar(grid, renderer, lights)


  def updateAStarKey(self, current, target, neighbor_key, cost):
    # calculate new g_score previous + cost cost of tile
    new_g_score = self._g_score[current] + cost

    # checking if state ain't in g_score register and if new one is better then previous
    if neighbor_key not in self._g_score or new_g_score < self._g_score[neighbor_key]:
      self._g_score[neighbor_key] = new_g_score                                      # adding/updating to lowest g_score for state
      f_score = new_g_score + self.calculateDistance(neighbor_key[0], target)  # calculating f_score = g_score + heuristic
      heapq.heappush(self._open_set, (f_score, neighbor_key))                        # adding to priority queue base on f_score = g_score + heuristic 
      self._came_from[neighbor_key] = current                                        # adding to graph


  def prepareAStar(self, current_position):
    if(self._target is None): return
    
    # start
    self._searching_for_path = True
    self._start_pos = tuple(current_position)
    self._target_pos = tuple(self._target)
    
    start_r = self._rotation
    self._start_key = (self._start_pos, start_r)

    self._goal_node = None

    # priority queue for A*
    self._open_set = []
    heapq.heappush(self._open_set, (0, self._start_key))
    self._g_score = {self._start_key: 0}
    self._visited = set()

    # graph
    self._came_from = {}


  def stepAStar(self, grid, renderer, lights):
    if(len(self._open_set) == 0): return
    if(self._searching_for_path == False): return

    # getting tile from priority queue
    _, current = heapq.heappop(self._open_set)
    current_pos, current_r = current
    
    if(SEARCH_VISUALIZATION):
      self._visualize[current] = Object(-10, EXPLORED_TEXTURE, np.array(current_pos), [0, TILE_SIZE])

    # checking if we reach target
    if current_pos == self._target_pos:
      self._goal_node = current
      self.recreatePathAStar(grid, renderer, lights)
      return

    # checking if we already check this state
    if current in self._visited:
      return
    
    # adding current to visited list
    self._visited.add(current)

    # get neighbors from precomputed grid
    list_of_possible_movement = grid.getNeighbors(current_pos)

    # getting neighbor position when we go forward
    d = BEING_MOVEMENT_DIRECTIONS[current_r]
    neighbor_pos = (current_pos[0] + int(d[0]), current_pos[1] + int(d[1]))
    
    # check if forward neighbor is in possible movements precomputed in grid
    if neighbor_pos in list_of_possible_movement:
      # generate new key
      neighbor_key = (neighbor_pos, current_r)
      
      # update key
      cost = grid.getCost(neighbor_pos)
      self.updateAStarKey(current, self._target_pos, neighbor_key, cost)
      if neighbor_key not in self._visited:
        if(SEARCH_VISUALIZATION):
          self._visualize[current] = Object(-10, TO_CHECK_TEXTURE, np.array(current_pos), [0, TILE_SIZE])

    # generate new key for left rotation
    new_r = (current_r - 1) % 4
    neighbor_key = (current_pos, new_r)
    # update key
    self.updateAStarKey(current, self._target_pos, neighbor_key, BEING_DEFAULT_ROTATE_COST)

    if neighbor_key not in self._visited:
      if(SEARCH_VISUALIZATION):
        self._visualize[current] = Object(-10, TO_CHECK_TEXTURE, np.array(current_pos), [0, TILE_SIZE])

    # generate new key for right rotation
    new_r = (current_r + 1) % 4
    neighbor_key = (current_pos, new_r)
    # update key
    self.updateAStarKey(current, self._target_pos, neighbor_key, BEING_DEFAULT_ROTATE_COST)

    if neighbor_key not in self._visited:
      if(SEARCH_VISUALIZATION):
        self._visualize[current] = Object(-10, TO_CHECK_TEXTURE, np.array(current_pos), [0, TILE_SIZE])


  def recreatePathAStar(self, grid, renderer, lights) -> None:
    if self._goal_node is None:
      if(DEBUG): print("No path found!")
      self._path = []
      return
    
    final_path = []
    temp = self._goal_node

    # move through came_from to start
    while temp != self._start_key:
      final_path.append(temp)
      temp = self._came_from[temp]

      if(SEARCH_VISUALIZATION):
        temp_pos, temp_r = temp
        self._visualize[temp_pos] = Object(-10, CORRECT_TEXTURE, np.array(temp_pos), [0, TILE_SIZE])
        self._visualize[temp_pos].render(renderer.getSurface(), grid, renderer, lights)
        renderer._surface.blit(renderer._world_surface, (0, 0), renderer._camera.getRect())
        pygame.display.flip()

    # reverse path
    self._path = final_path[::-1]
    self._path_found = True
    self._searching_for_path = False
    self._visualize.clear()



  def updateBFSKey(self, current, neighbor_key):
    if neighbor_key not in self._came_from:
      self._queue.append(neighbor_key)           # add to queue 
      self._came_from[neighbor_key] = current    # adding to graph


  def prepareBFS(self, current_position):
    if(self._target is None): return
    
    # start
    self._searching_for_path = True
    start_pos = tuple(current_position)
    self._target_pos = tuple(self._target)
    
    start_r = self._rotation
    self._start_key = (start_pos, start_r)

    self._goal_node = None

    # queue for BFS
    self._queue = deque()
    self._queue.append(self._start_key)
    self._visited = set()

    # graph
    self._came_from = {}
    

  def stepBFS(self, grid, renderer, lights):
    # getting tile from priority queue
    current = self._queue.popleft()
    current_pos, current_r = current

    if(SEARCH_VISUALIZATION):
      self._visualize[current] = Object(-10, EXPLORED_TEXTURE, np.array(current_pos), [0, TILE_SIZE])

    # checking if we reach target
    if current_pos == self._target_pos:
      self._goal_node = current
      self.recreateBFS(grid, renderer, lights)
      return

    # checking if we already check this state
    if current in self._visited:
      return
    
    # adding current to visited list
    self._visited.add(current)

    # get neighbors from precomputed grid
    list_of_possible_movement = grid.getNeighbors(current_pos)

    # getting neighbor position when we go forward
    d = BEING_MOVEMENT_DIRECTIONS[current_r]
    neighbor_pos = (current_pos[0] + int(d[0]), current_pos[1] + int(d[1]))
    
    # check if forward neighbor is in possible movements precomputed in grid
    if neighbor_pos in list_of_possible_movement:
      # generate new key
      neighbor_key = (neighbor_pos, current_r)
      
      # update key
      self.updateBFSKey(current, neighbor_key)

      if neighbor_key not in self._visited:
        if(SEARCH_VISUALIZATION):
          self._visualize[current] = Object(-10, TO_CHECK_TEXTURE, np.array(current_pos), [0, TILE_SIZE])

    # generate new key for left rotation
    new_r = (current_r - 1) % 4
    neighbor_key = (current_pos, new_r)
    # update key
    self.updateBFSKey(current, neighbor_key)

    if neighbor_key not in self._visited:
      if(SEARCH_VISUALIZATION):
        self._visualize[current] = Object(-10, TO_CHECK_TEXTURE, np.array(current_pos), [0, TILE_SIZE])

    # generate new key for right rotation
    new_r = (current_r + 1) % 4
    neighbor_key = (current_pos, new_r)
    # update key
    self.updateBFSKey(current, neighbor_key)

    if neighbor_key not in self._visited:
      if(SEARCH_VISUALIZATION):
        self._visualize[current] = Object(-10, TO_CHECK_TEXTURE, np.array(current_pos), [0, TILE_SIZE])


  def recreateBFS(self, grid, renderer, lights) -> None:
    if self._goal_node is None:
      if(DEBUG): print("No path found!")
      self._path = []
      return
    
    final_path = []
    temp = self._goal_node

    # move through came_from to start
    while temp != self._start_key:
      final_path.append(temp)
      temp = self._came_from[temp]

      if(SEARCH_VISUALIZATION):
        temp_pos, temp_r = temp
        self._visualize[temp] = Object(-10, CORRECT_TEXTURE, np.array(temp_pos), [0, TILE_SIZE])


    # reverse path
    self._path = final_path[::-1]
    self._path_found = True
    self._searching_for_path = False
    self._visualize.clear()



  def makeStep(self, deltaTime: float, acceleration: float) -> None:
    if not self._path or self._path_found == False or self._searching_for_path == True: 
      self._accTime = 0
      return

    next_pos, next_r = self._path[0]
    
    current_pos = tuple(self.getPosition())

    if next_pos == current_pos:
      # rotate
      if DEBUG: 
        directions = {0: 'north', 1: 'east', 2: 'south', 3: 'west'}
        print(f"New rotation: {directions.get(next_r, 'unknown')}")
      self._rotation = next_r
      self._path.pop(0)
    else:
      # move
      self._accTime += deltaTime
      dist = 1.0 
      
      if self._accTime >= dist / (self._velocity * acceleration):
        self.setPosition(list(next_pos))
        self._rotation = next_r
        self._path.pop(0)
        self._accTime = 0
        self.lit_surface = None
