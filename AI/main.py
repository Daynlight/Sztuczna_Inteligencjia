from Classes.Window import Window
from Classes.Object import objectMap
from Classes.Grid import Grid
from Classes.World import World

from initscene import *
from conf import *
import pygame


env = Window("Kelner Window", WINDOW_WIDTH, WINDOW_HEIGHT)
world = World(WORLD_WIDTH, WORLD_HEIGHT)
grid = Grid(GRID_X, GRID_Y , gridSize, MARGIN_HORIZONTAL, MARGIN_VERTICAL)
grid.walles = [Wall(grid.nodes[0][0], grid.nodes[GRID_Y][0], 50),
         Wall(grid.nodes[0][0], grid.nodes[0][GRID_X], 50)]

def render(window, grid):

  env.camera.update()                                  #update the position of camera
  camera_rect = env.camera.camera
  world.draw()                                         #draw world surface
  env.PoolEvents(world)                                #handling events
  if(env.mouseButtonDown):                             #for now, waiter movement
    mouse_pos = pygame.mouse.get_pos()
    hovered_tile = grid.get_hovered_tile(mouse_pos, env.camera)

    if hovered_tile:
      kelner.goTo(hovered_tile)

  grid.draw(world.surface)                              #draw grid

  kelner.makeStep(env.deltaTime)                        #sth for path-finding

  for el in sorted(objectMap.values(), key=lambda e: e.render_order): #drawing objects
    el.render(world.surface, grid)

  window.blit(world.surface, (0, 0), area = camera_rect) #final dispaly like window.display() in cpp


#MAIN LOOP


while(env.running):
  render(env.window, grid)
  
  env.SwapBuffer()

pygame.quit()