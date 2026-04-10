import pygame
import numpy as np
from conf import *
from .Grid import Grid, Tile


objectMap = {}

class Object:
  def __init__(self, name, render_order, texture_path, position: np.array, size: np.array):
    self.path = []
    self.render_order = render_order
    self.name = name
    self.setTexture(texture_path, size)
    self.setPosition(position)
    objectMap[name] = self
    self.accTime = 0

  def __del__(self):
    if self.name in objectMap:
      del objectMap[self.name]
  
  def setPosition(self, position: np.array):
    self.position = np.array(position, dtype=int)

  def setSize(self, size: np.array):
    self.size = np.array(size, dtype=int)
    self.texture = pygame.transform.scale(self.texture, self.size * gridSize)

  def setTexture(self, texture_path, size: np.array):
    self.texture_path = texture_path
    self.texture = pygame.image.load(self.texture_path)
    self.setSize(size)

  def goTo(self, hovered_tile : Tile): #position array[x, y]
    self.generatePath(self.position, hovered_tile)

  def calculateDistance(self, current_position: np.array, position: np.array):
    return np.linalg.norm(np.array(current_position) - np.array(position))
  
  def generatePath(self, current_position: np.array, position):
    start = np.array(current_position)
    target = np.array([position.isometric_x, position.isometric_y])

    directions = [
        np.array([1, 0]),
        np.array([-1, 0]),
        np.array([0, 1]),
        np.array([0, -1]),
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
          self.name != el.name and np.array_equal(el.position, np.array(neighbor))
          for el in objectMap.values()
        )
        if collision:
          continue

        tentative_g = g_score[current] + 1  # cost to move = 1 per step

        if neighbor not in g_score or tentative_g < g_score[neighbor]:
          g_score[neighbor] = tentative_g
          f_score = tentative_g + self.calculateDistance(neighbor, target_key)
          heapq.heappush(open_set, (f_score, neighbor))
          came_from[neighbor] = current

    final_path = []
    temp = target_key
    if temp not in came_from:
      print("No path found!")
      self.path = []
      return

    while temp != start_key:
      final_path.append(np.array(temp))
      temp = came_from[temp]

    self.path = final_path[::-1]

  def makeStep(self, deltaTime: float):
    if(len(self.path) <= 0): 
      self.accTime = 0
      return

    self.accTime += deltaTime
    if(self.accTime >= 1/self.velocity):
      self.position = self.path[0]
      self.path.pop(0)
      self.accTime -= self.accTime

  def render(self, window: pygame.Surface, grid : Grid):
    tile = grid.tiles[self.position[0]][self.position[1]]
    x = tile.left_corner.get()[0] + tile.a/2
    y = tile.left_corner.get()[1] - tile.a

    window.blit(self.texture, (x, y))
