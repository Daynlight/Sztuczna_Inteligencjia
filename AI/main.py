from Classes.Window import Window
from Classes.Object import objectMap
from Classes.Grid import Grid, Tile

from initscene import *
from conf import *
import pygame


env = Window("Kelner Window", WINDOW_WIDTH, WINDOW_HEIGHT)

grid = Grid(GRID_X, GRID_Y , gridSize, 50, 0)

def render(window, grid):
  window.fill((255, 0, 0)) #background color

  if(env.mouseButtonDown):
    mouse_pos = pygame.mouse.get_pos()
    hovered_tile = grid.get_hovered_tile(mouse_pos)

    if hovered_tile:
      print(hovered_tile.isometric_x, hovered_tile.isometric_y)
      kelner.goTo(hovered_tile)

  grid.draw(env.window)

  kelner.makeStep(env.deltaTime)
  for el in objectMap.values():
    el.render(window, grid)


clock = pygame.time.Clock()

#MAIN LOOP


while(env.running):
  env.deltaTime = clock.tick(60) / 1000.0 
  render(env.window, grid)
  
  env.SwapBuffer()
  env.PoolEvents()

pygame.quit()