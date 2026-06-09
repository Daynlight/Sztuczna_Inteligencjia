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
  

  def pathIsEmpty(self):
    return len(self._path) == 0


  def goTo(self, grid, goal, renderer, lights) -> None:
    if goal is None: 
      return
    
    self._visualize = {}
    
    target = self._find_adjacent_target(grid, goal)
    match PATH_SEARCH_VARIANT:
      case PATH_SEARCH_VARIANTS.A_STAR:
        self.generatePathAStar(grid, self.getPosition(), target, renderer, lights)
      case PATH_SEARCH_VARIANTS.BFS:
        self.generatePathBFS(grid, self.getPosition(), target, renderer, lights)
      case _:
        self.generatePathAStar(grid, self.getPosition(), target, renderer, lights)


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


  def updateAStarKey(self, current, target, neighbor_key, cost, g_score, open_set, came_from):
    # calculate new g_score previous + cost cost of tile
    new_g_score = g_score[current] + cost

    # checking if state ain't in g_score register and if new one is better then previous
    if neighbor_key not in g_score or new_g_score < g_score[neighbor_key]:
      g_score[neighbor_key] = new_g_score                                      # adding/updating to lowest g_score for state
      f_score = new_g_score + self.calculateDistance(neighbor_key[0], target)  # calculating f_score = g_score + heuristic
      heapq.heappush(open_set, (f_score, neighbor_key))                        # adding to priority queue base on f_score = g_score + heuristic 
      came_from[neighbor_key] = current                                        # adding to graph


  def updateBFSKey(self, current, neighbor_key, queue, came_from):
    if neighbor_key not in came_from:
      queue.append(neighbor_key)           # add to queue 
      came_from[neighbor_key] = current    # adding to graph


  def generatePathAStar(self, grid, current_position: np.ndarray[int], target, renderer, lights) -> None:
    if(target is None): return
    
    # start
    start_pos = tuple(current_position)
    target_pos = tuple(target)
    
    start_r = self._rotation
    start_key = (start_pos, start_r)

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
      
      if(SEARCH_VISUALIZATION):
        self._visualize[current] = Object(10, EXPLORED_TEXTURE, np.array(current_pos), [0, TILE_SIZE])
        self._visualize[current].render(renderer.getSurface(), grid, renderer, lights)
        renderer._surface.blit(renderer._world_surface, (0, 0), renderer._camera.getRect())
        pygame.display.flip()

      # checking if we reach target
      if current_pos == target_pos:
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
      neighbor_pos = (current_pos[0] + int(d[0]), current_pos[1] + int(d[1]))
      
      # check if forward neighbor is in possible movements precomputed in grid
      if neighbor_pos in list_of_possible_movement:
        # generate new key
        neighbor_key = (neighbor_pos, current_r)
        
        # update key
        cost = grid.getCost(neighbor_pos)
        self.updateAStarKey(current, target_pos, neighbor_key, cost, g_score, open_set, came_from)
        if neighbor_key not in visited:
          if(SEARCH_VISUALIZATION):
            self._visualize[current] = Object(10, TO_CHECK_TEXTURE, np.array(current_pos), [0, TILE_SIZE])
            self._visualize[current].render(renderer.getSurface(), grid, renderer, lights)
            renderer._surface.blit(renderer._world_surface, (0, 0), renderer._camera.getRect())
            pygame.display.flip()

      # generate new key for left rotation
      new_r = (current_r - 1) % 4
      neighbor_key = (current_pos, new_r)
      # update key
      self.updateAStarKey(current, target_pos, neighbor_key, BEING_DEFAULT_ROTATE_COST, g_score, open_set, came_from)

      if neighbor_key not in visited:
        if(SEARCH_VISUALIZATION):
          self._visualize[current] = Object(10, TO_CHECK_TEXTURE, np.array(current_pos), [0, TILE_SIZE])
          self._visualize[current].render(renderer.getSurface(), grid, renderer, lights)
          renderer._surface.blit(renderer._world_surface, (0, 0), renderer._camera.getRect())
          pygame.display.flip()

      # generate new key for right rotation
      new_r = (current_r + 1) % 4
      neighbor_key = (current_pos, new_r)
      # update key
      self.updateAStarKey(current, target_pos, neighbor_key, BEING_DEFAULT_ROTATE_COST, g_score, open_set, came_from)

      if neighbor_key not in visited:
        if(SEARCH_VISUALIZATION):
          self._visualize[current] = Object(10, TO_CHECK_TEXTURE, np.array(current_pos), [0, TILE_SIZE])
          self._visualize[current].render(renderer.getSurface(), grid, renderer, lights)
          renderer._surface.blit(renderer._world_surface, (0, 0), renderer._camera.getRect())
          pygame.display.flip()

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

      if(SEARCH_VISUALIZATION):
        temp_pos, temp_r = temp
        self._visualize[temp] = Object(10, CORRECT_TEXTURE, np.array(temp_pos), [0, TILE_SIZE])
        self._visualize[temp].render(renderer.getSurface(), grid, renderer, lights)
        renderer._surface.blit(renderer._world_surface, (0, 0), renderer._camera.getRect())
        pygame.display.flip()

    # reverse path
    self._path = final_path[::-1]

    if(SEARCH_VISUALIZATION):
      pygame.time.wait(1000)
    
    self._visualize.clear()


  def generatePathBFS(self, grid, current_position: np.ndarray[int], target, renderer, lights) -> None:
    if(target is None): return
    
    # start
    start_pos = tuple(current_position)
    target_pos = tuple(target)
    
    start_r = self._rotation
    start_key = (start_pos, start_r)

    goal_node = None

    # queue for BFS
    queue = deque()
    queue.append(start_key)
    visited = set()

    # graph
    came_from = {}
    
    while len(queue) > 0:
      # getting tile from priority queue
      current = queue.popleft()
      current_pos, current_r = current

      if(SEARCH_VISUALIZATION):
        self._visualize[current] = Object(10, EXPLORED_TEXTURE, np.array(current_pos), [0, TILE_SIZE])
        self._visualize[current].render(renderer.getSurface(), grid, renderer, lights)
        renderer._surface.blit(renderer._world_surface, (0, 0), renderer._camera.getRect())
        pygame.display.flip()

      # checking if we reach target
      if current_pos == target_pos:
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
      neighbor_pos = (current_pos[0] + int(d[0]), current_pos[1] + int(d[1]))
      
      # check if forward neighbor is in possible movements precomputed in grid
      if neighbor_pos in list_of_possible_movement:
        # generate new key
        neighbor_key = (neighbor_pos, current_r)
        
        # update key
        self.updateBFSKey(current, neighbor_key, queue, came_from)

        if neighbor_key not in visited:
          if(SEARCH_VISUALIZATION):
            self._visualize[current] = Object(10, TO_CHECK_TEXTURE, np.array(current_pos), [0, TILE_SIZE])
            self._visualize[current].render(renderer.getSurface(), grid, renderer, lights)
            renderer._surface.blit(renderer._world_surface, (0, 0), renderer._camera.getRect())
            pygame.display.flip()

      # generate new key for left rotation
      new_r = (current_r - 1) % 4
      neighbor_key = (current_pos, new_r)
      # update key
      self.updateBFSKey(current, neighbor_key, queue, came_from)

      if neighbor_key not in visited:
        if(SEARCH_VISUALIZATION):
          self._visualize[current] = Object(10, TO_CHECK_TEXTURE, np.array(current_pos), [0, TILE_SIZE])
          self._visualize[current].render(renderer.getSurface(), grid, renderer, lights)
          renderer._surface.blit(renderer._world_surface, (0, 0), renderer._camera.getRect())
          pygame.display.flip()

      # generate new key for right rotation
      new_r = (current_r + 1) % 4
      neighbor_key = (current_pos, new_r)
      # update key
      self.updateBFSKey(current, neighbor_key, queue, came_from)

      if neighbor_key not in visited:
        if(SEARCH_VISUALIZATION):
          self._visualize[current] = Object(10, TO_CHECK_TEXTURE, np.array(current_pos), [0, TILE_SIZE])
          self._visualize[current].render(renderer.getSurface(), grid, renderer, lights)
          renderer._surface.blit(renderer._world_surface, (0, 0), renderer._camera.getRect())
          pygame.display.flip()

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

      if(SEARCH_VISUALIZATION):
        temp_pos, temp_r = temp
        self._visualize[temp] = Object(10, CORRECT_TEXTURE, np.array(temp_pos), [0, TILE_SIZE])
        self._visualize[temp].render(renderer.getSurface(), grid, renderer, lights)
        renderer._surface.blit(renderer._world_surface, (0, 0), renderer._camera.getRect())
        pygame.display.flip()


    # reverse path
    self._path = final_path[::-1]

    if(SEARCH_VISUALIZATION):
      pygame.time.wait(1000)
    
    self._visualize.clear()


  def makeStep(self, deltaTime: float, acceleration: float) -> None:
    if not self._path: 
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
