import pygame
import numpy as np

from Classes.Grid.Grid import Grid, Grid_Tile
from Classes.Renderer.Renderer import Renderer, Camera

from conf import TILE_SIZE, ERROR_TEXTURE, WINDOW_WIDTH, WINDOW_HEIGHT

# Main superior class for all objects in the world

class Object:
  def __init__(self, render_order: int, texture_path: str, position: np.ndarray[int], 
               offset: np.ndarray[int] = np.array([0, 0], dtype=int), size: np.ndarray[int] = np.array([1, 1], dtype=int)):
    self._position: np.ndarray[int] = position
    self._size: np.ndarray[int] = size

    self._offset: np.ndarray[int] = offset
    self._render_order: int = render_order
    
    self._texture_path: str = texture_path
    self._texture: pygame.Surface = None

  
  def _isVisible(self, grid_tile: Grid_Tile, renderer: Renderer) -> bool:
    render_pos: np.ndarray[int] = grid_tile.getRenderPos()
    camera: Camera = renderer.getCamera()
    viewport = [render_pos[0] - camera.getRect().x, render_pos[1] - camera.getRect().y]

    if(viewport[0] + self._size[0] * TILE_SIZE + self._offset[0] < 0): return False
    if(viewport[1] + self._size[1] * TILE_SIZE + self._offset[1] < 0): return False
    if(viewport[0] > WINDOW_WIDTH): return False
    if(viewport[1] > WINDOW_HEIGHT): return False

    return True


  def render(self, surface: pygame.Surface, grid : Grid, renderer: Renderer) -> None:
    if(self._texture == None): 
      self.setTexture(self._texture_path)
      self.setSize(self._size)

    grid_tile: Grid_Tile = grid._grid_tiles[self._position[0]][self._position[1]]   # each object is drawn on top of some tile
    render_pos: np.ndarray[int] = grid_tile.getRenderPos()                          # changing tile coordinates for example [2,2] -> to world coordinates 

    if(self._isVisible(grid_tile, renderer)):
      surface.blit(self._texture, render_pos + self._offset)                        # drawing object + offset
  

  def setPosition(self, position: np.ndarray[int]) -> None:
    self._position: np.ndarray[int] = position


  def setSize(self, size: np.ndarray[int]) -> None:
    # setting size of the texture in the world
    
    self._size: np.ndarray[int] = size
    transform_size: tuple = (self._size[0] * TILE_SIZE, self._size[1] * TILE_SIZE)
    self._texture: pygame.Surface = pygame.transform.scale(self._texture, transform_size)


  def setTexture(self, texture_path: str) -> None:
    self._texture_path = texture_path
    try:
        self._texture = pygame.image.load(self._texture_path)
    except (pygame.error, FileNotFoundError) as e:
        print(f"Failed to load {self._texture_path}: {e}.")
        self._texture = ERROR_TEXTURE

  
  def getPosition(self) -> np.ndarray[int]:
    return self._position
  

  def getRenderOrder(self) -> int:
    return self._render_order
