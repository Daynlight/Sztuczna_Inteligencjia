from Classes.Window import Window
from Classes.Object import objectMap
from initscene import *






env = Window("Kelner Window")



def render(window):
  window.fill((255, 0, 0))
  if(env.mouseButtonDown):
    kelner.goTo(env.mousePosition - kelner.size // 2)

  kelner.makeStep(env.deltaTime)
  for el in objectMap.values():
    el.render(window)



env.loop(render)
