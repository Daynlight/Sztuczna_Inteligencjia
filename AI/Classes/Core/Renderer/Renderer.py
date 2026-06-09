import pygame
import numpy as np
import time

from conf import WORLD_HEIGHT, WORLD_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH, CAMERA_SPEED









class Camera:
  def __init__(self, width: int, height: int, center_x_pos: int, center_y_pos: int):
    self._rect: pygame.Rect = pygame.Rect(0, 0, width, height)
    self._size: np.ndarray[int] = np.array([width, height], dtype=int)
    self._center: np.ndarray[int] = np.array([center_x_pos, center_y_pos], dtype=int)
    
    self._update()


  def _update(self) -> None:
    self._rect.x = self._center[0] - self._size[0] // 2
    self._rect.y = self._center[1] - self._size[1] // 2


  def getCenter(self) -> np.ndarray[int]:
    return self._center
  

  def getRect(self) -> pygame.Rect:
    return self._rect
  

  def adjustCenter(self, center_x: int, center_y: int) -> None:
    if(center_x != None): self._center[0] += center_x
    if(center_y != None): self._center[1] += center_y
    
    self._update()


  def setCenter(self, center_x: int, center_y: int) -> None:
    if(center_x != None): self._center[0] = center_x
    if(center_y != None): self._center[1] = center_y
    
    self._update()









class Renderer:
  def __init__(self, title: str, width: int, height: int):
    self._running: bool = True
    self._title: str = title
    self._size: np.ndarray[int] = np.array([width, height], dtype=int)
    self._surface: pygame.Surface = None
    self._world_surface: pygame.Surface = None
    self._camera: Camera = None

    self._events: np.ndarray[pygame.event.Event] = None
    self._event_keys: np.ndarray[np.int_] = None
    self._clock: time.time = None
    self._deltaTime: float = 0.0

    self._mousePosition: np.ndarray[int] = None
    self._mouseButtonDown: bool = False

    pygame.init()


  def __del__(self):
    pygame.quit()


  def _createSurface(self) -> None:
    self._surface: pygame.Surface = pygame.display.set_mode((self._size[0], self._size[1]), vsync=0)
    pygame.display.set_caption(self._title)


  def _createWorldSurface(self) -> None:
    self._world_surface: pygame.Surface = pygame.Surface((WORLD_WIDTH, WORLD_HEIGHT))


  def _createCamera(self) -> None:
    if(self._camera == None): self._camera: Camera = Camera(self._size[0], self._size[1], WORLD_WIDTH / 2, WORLD_HEIGHT / 2)


  def _pollEvents(self) -> None:
    if(self._surface == None): self._createSurface()
    if(self._camera == None): self._createCamera()

    self._events: np.ndarray[pygame.event.Event] = pygame.event.get()
    self._event_keys: np.ndarray[np.int_] = pygame.key.get_pressed()

    for event in self._events:
      if event.type == pygame.QUIT:
        self._running: bool = False

    self._cameraEvents()
    self._mouseEvents()


  def _mouseEvents(self) -> None:
    if(self._events == None): return

    self._mouseButtonDown: bool = False
    for event in self._events:
      if event.type == pygame.MOUSEBUTTONDOWN:
        self._mouseButtonDown: bool = True
        self._mousePosition: np.ndarray[int] = event.pos


  def _cameraEvents(self) -> None:
    if(self._events == None): return
    if(self._camera == None): self._createCamera()

    center: np.ndarray[int] = self._camera.getCenter()
    
    if self._event_keys[pygame.K_w]:
      if(center[1] > WINDOW_HEIGHT // 2):
        self._camera.adjustCenter(None, -CAMERA_SPEED * self._deltaTime)
      else:
        self._camera.setCenter(None, WINDOW_HEIGHT // 2)

    if self._event_keys[pygame.K_s]:
      if(center[1] < WORLD_HEIGHT - WINDOW_HEIGHT // 2):
        self._camera.adjustCenter(None, CAMERA_SPEED * self._deltaTime)
      else:
        self._camera.setCenter(None, WORLD_HEIGHT - WINDOW_HEIGHT // 2)

    if self._event_keys[pygame.K_a]:
      if (center[0] > WINDOW_WIDTH // 2):
        self._camera.adjustCenter(-CAMERA_SPEED * self._deltaTime, None)
      else:
        self._camera.setCenter(WINDOW_WIDTH // 2, None)

    if self._event_keys[pygame.K_d]:
      if(center[0] < WORLD_WIDTH - WINDOW_WIDTH // 2):
        self._camera.adjustCenter(CAMERA_SPEED * self._deltaTime, None)
      else:
        self._camera.setCenter(WORLD_WIDTH - WINDOW_WIDTH // 2, None)


  def backgroundColor(self, color: np.ndarray[int]) -> None:
    if(self._world_surface == None): self._createWorldSurface()
    self._world_surface.fill(color)


  def renderFrame(self) -> None:
    if(self._surface == None): self._createSurface()
    if(self._world_surface == None): self.createWorldSurface()
    if(self._camera == None): self._createCamera()
    if(self._clock == None): self._clock = time.time()

    self._surface.blit(self._world_surface, (0, 0), self._camera.getRect())
    
    pygame.display.flip()

    self._deltaTime: float =  (time.time() - self._clock)
    self._clock = time.time()

    self._pollEvents()


  def getSurface(self) -> pygame.Surface:
    if(self._world_surface == None): self._createWorldSurface()
    return self._world_surface

  
  def getMouse(self) -> np.ndarray[int]:
    if(self._mouseButtonDown == None or self._mouseButtonDown == False): return None
    if(self._mousePosition == None): return None
    return self._mousePosition
  

  def getDeltaTime(self) -> float:
    if(self._deltaTime == None): return 0.0
    return self._deltaTime
  

  def getRunning(self) -> bool:
    if(self._running == None): return False
    return self._running
  

  def getCamera(self) -> Camera:
    if(self._camera == None): self._createCamera()
    return self._camera
