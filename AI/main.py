import time
from Classes.Model import Model









model = Model()
for i in range(200):
  model.modelIteration(2000)

while(model.isRunning()):
  model.modelIteration()
  model.renderFrame()
  