from Classes.Model import Model


model = Model()


while(model.isRunning()):
  model.modelIteration()

  model.renderFrame()
  
  
  