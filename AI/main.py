import time
from Classes.Model import Model









model = Model()
# for i in range(200):
#   model.modelIteration(2000)

reg = []
while(model.isRunning()):
  begging = time.time()
  model.modelIteration()
  model.renderFrame()
  end = time.time()
  
  reg.append((end - begging))
  if(len(reg) >= 200):
    print("[FPS]:", 1/(sum(reg)/len(reg)))
    reg.clear()
  