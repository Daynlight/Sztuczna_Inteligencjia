from Classes.Window import Window
from Classes.Object import objectMap
from initscene import *
from conf import *


env = Window("Kelner Window", WINDOW_WIDTH, WINDOW_LENGTH)



def render(window):
  window.fill((255, 0, 0)) #background color
  if(env.mouseButtonDown):
    kelner.goTo(env.mousePosition - kelner.size // 2)

  kelner.makeStep(env.deltaTime)
  for el in objectMap.values():
    el.render(window)



env.loop(render)
