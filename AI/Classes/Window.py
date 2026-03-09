import pygame
from typing import Callable
import sys
import conf
from Classes.World import Camera, World

class Window:
  def __init__(self, title: str, width, height):
    self.running = True
    self.window = None
    self.mousePosition = None
    self.mouseButtonDown = False
    self.deltaTime = 0
    self.camera = Camera(width, height, conf.WORLD_WIDTH / 2, conf.WORLD_HEIGHT / 2)

    pygame.init()
    self.CreateWindow(title, width, height)

  def __del__(self):
    pygame.quit()

  def CreateWindow(self, title: str, width, height):
    self.window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

  def PoolEvents(self, world: World):

    self.mouseButtonDown = False

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      
      if event.type == pygame.MOUSEBUTTONDOWN:
        self.mouseButtonDown = True
        self.mousePosition = event.pos


    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
      if(self.camera.center_y_pos > conf.WINDOW_HEIGHT // 2):
        self.camera.center_y_pos -= 10

    if keys[pygame.K_DOWN]:
      if(self.camera.center_y_pos < conf.WORLD_HEIGHT - conf.WINDOW_HEIGHT // 2):
        self.camera.center_y_pos += 10

    if keys[pygame.K_LEFT]:
      if (self.camera.center_x_pos > conf.WINDOW_WIDTH // 2):
        self.camera.center_x_pos -= 10

    if keys[pygame.K_RIGHT]:
      if(self.camera.center_x_pos < conf.WORLD_WIDTH - conf.WINDOW_WIDTH // 2):
        self.camera.center_x_pos += 10


  def SwapBuffer(self):
    pygame.display.flip()

    clock = pygame.time.Clock()
    self.deltaTime = clock.tick(60) / 1000.0 
