from Classes.Window import Window
from Classes.Object import objectMap
from Classes.Grid import Grid

from initscene import *
import conf
import pygame


env = Window("Kelner Window", conf.WINDOW_WIDTH, conf.WINDOW_HEIGHT)

grid = Grid(10,10,40)

def render(window):
  window.fill((255, 0, 0)) #background color
  if(env.mouseButtonDown):
    kelner.goTo(env.mousePosition - kelner.size // 2)

  kelner.makeStep(env.deltaTime)
  for el in objectMap.values():
    el.render(window)


clock = pygame.time.Clock()

#MAIN LOOP


while(env.running):
  env.deltaTime = clock.tick(60) / 1000.0 
  render(env.window)
  grid.draw(env.window)
  
  env.DrawGridLines()
  env.SwapBuffer()
  env.PoolEvents()

pygame.quit()