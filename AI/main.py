from Classes.Window import Window
from Classes.Object import objectMap
from initscene import *
from conf import *
import pygame


env = Window("Kelner Window", WINDOW_WIDTH, WINDOW_LENGTH)



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
  env.SwapBuffer()
  env.PoolEvents()

pygame.quit()