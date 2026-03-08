import pygame
from typing import Callable
import sys






class Window:
  def __init__(self, title: str, width, height):
    self.running = True
    self.window = None
    self.mousePosition = None
    self.mouseButtonDown = False
    self.deltaTime = 0
    pygame.init()
    self.CreateWindow(title, width, height)

  def __del__(self):
    pygame.quit()

  def CreateWindow(self, title: str, width, height):
    self.window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

  def PoolEvents(self):

    self.mouseButtonDown = False

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      
      if event.type == pygame.MOUSEBUTTONDOWN:
        self.mouseButtonDown = True
        self.mousePosition = event.pos

  def SwapBuffer(self):
    pygame.display.flip()

  def loop(self, render: Callable[[pygame.Surface], None]):
    clock = pygame.time.Clock()
    while(self.running):
      self.deltaTime = clock.tick(60) / 1000.0 
      render(self.window)
      self.SwapBuffer()
      self.PoolEvents()

    pygame.quit()
