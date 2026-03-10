import pygame
import numpy as np
from conf import *
from .Grid import Grid


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

  def render(self, window: pygame.Surface, grid : Grid):
    tile = grid.tiles[self.position[0]][self.position[1]]
    x = tile.left_corner[0] + tile.a/2
    y = tile.left_corner[1] - tile.a

    window.blit(self.texture, (x, y))
