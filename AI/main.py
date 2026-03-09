from Classes.Window import Window
from Classes.Object import objectMap
from Classes.Grid import Grid
from Classes.World import World

from initscene import *
from conf import *
import pygame


env = Window("Kelner Window", WINDOW_WIDTH, WINDOW_HEIGHT)
world = World(WORLD_WIDTH, WORLD_HEIGHT)

grid = Grid(GRID_X, GRID_Y , gridSize, MARGIN_HORIZONTAL, MARGIN_VERTICAL) #Grid (x_tiles_number, y_tiles_number, tile_size, top_margin, left_margin)

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