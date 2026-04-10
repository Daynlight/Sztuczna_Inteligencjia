import pygame
import numpy as np
from conf import *
from .Grid import Grid, Tile


objectMap = {}

class Object:
  def __init__(self, name, render_order, texture_path, position: np.array, offset: np.array = [0, 0], size: np.array = [1, 1]):
    self.path = []
    self.render_order = render_order
    self.name = name
    self.offset = offset
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

    x = tile.bottom_corner.get()[0] - tile.a + self.offset[0]
    y = tile.bottom_corner.get()[1] - 2 * tile.a + self.offset[1]

    window.blit(self.texture, (x, y))
