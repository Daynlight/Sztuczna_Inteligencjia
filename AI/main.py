from Classes.Model import Model
from conf import FPS_SAMPLES



total_fps_sum = 0
total_fps_count = 0
fps_sum = 0
fps_count = 0



model = Model()
while(model.isRunning()):
  model.modelIteration()
  model.renderFrame()
  
  fps_sum += model._renderer._deltaTime
  total_fps_sum += model._renderer._deltaTime
  fps_count += 1
  total_fps_count += 1
  if(fps_sum >= FPS_SAMPLES):
    print("[FPS]:", 1/(fps_sum / fps_count))
    fps_count = 0
    fps_sum = 0



print("[Total AVG FPS]:", 1/(total_fps_sum / total_fps_count))
