import pygame
import numpy as np
from conf import *






objectMap = {}

class Object:
  def __init__(self, name, texture_path, position: np.array, velocity: float, size: np.array):
    self.path = []
    self.name = name
    self.velocity = float(velocity)
    self.setTexture(texture_path, size)
    self.setPosition(position)
    objectMap[name] = self

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

  def goTo(self, position: np.array): #position array[x, y]
    self.path = []
    if position[0] // gridSize < GRIDS_X and position[1] // gridSize < GRIDS_Y:
      self.generatePath(self.position, position // gridSize)

  def generatePath(self, current_position: np.array, position: np.array, depth = 20):
    self.path.append(position)

  def makeStep(self, deltaTime: float):
    if(len(self.path) <= 0): return
    self.position = self.path[0]
    self.path.pop(0)

  def render(self, window: pygame.Surface):
    window.blit(self.texture, self.position * gridSize)
