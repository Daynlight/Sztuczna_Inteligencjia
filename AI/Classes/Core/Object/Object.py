import pygame
import numpy as np

from Classes.Core.Grid.Grid import Grid, Grid_Tile
from Classes.Core.Renderer.Renderer import Renderer, Camera
from Classes.Core.Renderer.Texture import Texture
from Classes.Core.Animation.Animation import Animation
from Classes.Core.Renderer.Light import Light

from conf import TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT









# Main superior class for all objects in the world

class Object:
  def __init__(self, render_order: int, texture: Texture, position: np.ndarray[int] = [0, 0], 
               offset: np.ndarray[int] = np.array([0, 0], dtype=int), size: np.ndarray[int] = np.array([1, 1], dtype=int)):
    self._position: np.ndarray[int] = position
    self._size: np.ndarray[int] = size

    self._offset: np.ndarray[int] = offset
    self._render_order: int = render_order
    
    self._texture: Texture = texture
    self._animation: map[Animation] = {}
    self._state = None
    
    self.lit_surface: pygame.Surface = None
    self._last_pos = None

  
  def setAnimation(self, name, animation: Animation):
    self._animation[name] = animation


  def removeAnimation(self, name):
    self._animation[name] = None

  
  def setState(self, name: str):
    self._state = name


  def precomputeLight(self, grid: Grid, lights: np.ndarray[Light]):
    grid_tile: Grid_Tile = grid._grid_tiles[self._position[0]][self._position[1]]
    render_pos: np.ndarray[int] = grid_tile.getRenderPos()
    self.lit_surface = self._texture.precomputeLight(render_pos, lights)
    self._last_pos = render_pos

  
  def _isVisible(self, grid_tile: Grid_Tile, renderer: Renderer) -> bool:
    render_pos: np.ndarray[int] = grid_tile.getRenderPos()
    camera: Camera = renderer.getCamera()
    viewport = [render_pos[0] - camera.getRect().x, render_pos[1] - camera.getRect().y]

    if(viewport[0] + self._size[0] * TILE_SIZE + self._offset[0] < 0): return False
    if(viewport[1] + self._size[1] * TILE_SIZE + self._offset[1] < 0): return False
    if(viewport[0] + self._offset[0] > WINDOW_WIDTH): return False
    if(viewport[1] + self._offset[1] > WINDOW_HEIGHT): return False

    return True


  def render(self, surface: pygame.Surface, grid: Grid, renderer: Renderer, lights: np.ndarray[Light]) -> None:
    
    grid_tile: Grid_Tile = grid._grid_tiles[self._position[0]][self._position[1]]           # each object is drawn on top of some tile
    render_pos: np.ndarray[int] = grid_tile.getRenderPos()                                  # changing tile coordinates for example [2,2] -> to world coordinates
    
    if(self._isVisible(grid_tile, renderer)):
      if(self._animation != None and self._state != None):
        self.lit_surface = self._animation[self._state].getTexture(render_pos, lights, renderer.getDeltaTime())

      if(self.lit_surface == None or not np.array_equal(self._last_pos, render_pos)):
        self.lit_surface: pygame.Surface = self._texture.getLitTexture(render_pos, lights)
      
      self._last_pos = render_pos
      
      # If DYMANIC LIGHTS ARE TURNED OFF WORKS 2 TIMES SLOWER FOR SOME REASON
      surface.blit(self.lit_surface, render_pos + self._offset) # drawing object + offset# changing tile coordinates for example [2,2] -> to world coordinates

  
     


  def setPosition(self, position: np.ndarray[int]) -> None:
    self._position: np.ndarray[int] = position

  
  def getPosition(self) -> np.ndarray[int]:
    return self._position
  

  def getRenderOrder(self) -> int:
    return self._render_order
