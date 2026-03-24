import pygame
import numpy as np
from Classes.Renderer.Renderer import Camera, Renderer

from conf import TAIL_COLOR, TAIL_EDGE_COLOR, WALL_COLOR, WALL_EDGE_COLOR, WALL_HEIGHT, TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH




class Grid_Tile:
  #The most important part of object of class Grid_Tile is center_x and center_y, based on them is calulated rhombus (diament) with dimensions a x 2a 
  def __init__(self, center_x, center_y, a, isometric_x, isometric_y):
    self.center_x = center_x
    self.center_y = center_y
    self.a = a
    self.top_corner = None
    self.right_corner = None
    self.bottom_corner = None
    self.left_corner = None
    self.isometric_x = isometric_x
    self.isometric_y = isometric_y


  def __del__(self):
    self.top_corner = None
    self.right_corner = None
    self.bottom_corner = None
    self.left_corner = None


  def isHovered(self, mouse_pos: np.ndarray[int], camera : Camera) -> bool:
    x, y = mouse_pos

    world_x = x + camera.getRect().x
    world_y = y + camera.getRect().y

    dx = abs(world_x - self.center_x)
    dy = abs(world_y - self.center_y)

    if dx / self.a + dy / (self.a / 2) <= 1:
      return True
    return False
  

  def getRenderPos(self) -> np.ndarray[int]:
    x = self.bottom_corner[0] - self.a
    y = self.bottom_corner[1] - 2 * self.a
    return np.array([x, y], dtype=int)


  def draw(self, target_surface: pygame.Surface) -> None:
    pygame.draw.polygon(target_surface, TAIL_COLOR, (self.top_corner, self.right_corner, self.bottom_corner, self.left_corner))


  def isVisible(self, renderer: Renderer) -> bool:
    render_pos = self.getRenderPos()
    camera: Camera = renderer.getCamera()
    viewport = [render_pos[0] - camera.getRect().x, render_pos[1] - camera.getRect().y]

    if(viewport[0] + TILE_SIZE * 2 < 0): return False
    if(viewport[1] + TILE_SIZE * 2 < 0): return False
    if(viewport[0] > WINDOW_WIDTH): return False
    if(viewport[1] > WINDOW_HEIGHT): return False

    return True









## [TODO] change to matrix aka map with cords, 
# Use Matrices, 
# Two Grids, 
# Less Iterations, 
# Iterate though tails for rendering,
# Get neighbors for path finding,
# Get render point,
# Walls gen base on empty space behind with height,
class Grid:
  def __init__(self, size_x: int, size_y: int, grid_tile_size : int, margin_horizontal : int, margin_vertical: int):
    self._size: np.ndarray[int] = np.array([size_x, size_y], dtype=int)
    self._grid_tile_size: int = grid_tile_size
    self._margins: np.ndarray[int] = np.array([margin_horizontal, margin_vertical], dtype=int)
    self._grid_nodes: np.ndarray[np.ndarray[int]] = None
    self._grid_tiles: np.ndarray[np.ndarray[Grid_Tile]] = None

    self._generateGridNodes()
    self._generateGridTails()

    self._walls: np.ndarray[Wall] = np.array([
      Wall(self._grid_nodes[0][0], self._grid_nodes[self._size[1]][0], WALL_HEIGHT),
      Wall(self._grid_nodes[0][0], self._grid_nodes[0][self._size[0]], WALL_HEIGHT),
    ], dtype=Wall)


  def __del__(self):
    if(self._grid_tiles): self._grid_tiles.clear()


  def _generateGridNodes(self) -> None:
    # nodes that are used as the corners of the tiles
     
    if(self._grid_nodes != None): return
    
    self._grid_nodes = []

    for y in range(self._size[1] + 1):
      row = []

      for x in range(self._size[0] + 1):
        x_pos = self._margins[1] + (self._size[0] + x - y) * (self._grid_tile_size)
        y_pos = self._margins[0] + (x + y) * (self._grid_tile_size / 2) 
        grid_node = [x_pos, y_pos]
        row.append(grid_node)

      self._grid_nodes.append(row)


  def _generateGridTails(self) -> None:
    # generating the grid of tiles

    if(self._grid_tiles != None): return

    self._grid_tiles = []

    for y in range(0, self._size[1]):
      row = []

      for x in range(0, self._size[0]):
        grid_tile = Grid_Tile(
          self._margins[1] + ((self._size[0] + y - x)  * self._grid_tile_size), 
          self._margins[0] + (self._grid_tile_size / 2 + (y + x) * self._grid_tile_size/2), 
          self._grid_tile_size, 
          y, 
          x
        )

        # setting the position of all corneres of the tile (diamond)

        grid_tile.top_corner = self._grid_nodes[x][y]
        grid_tile.right_corner = self._grid_nodes[x][y + 1]
        grid_tile.bottom_corner = self._grid_nodes[x + 1][y + 1]
        grid_tile.left_corner = self._grid_nodes[x + 1][y] 
        row.append(grid_tile)

      self._grid_tiles.append(row)
        

  def get_hovered_tile(self, mouse_pos: np.ndarray[int], camera : Camera) -> Grid_Tile:
    # method to get the tile hovered by mouse, currently used to make the waiter go to selected tile

    for row in self._grid_tiles:
      for grid_tile in row:
        if grid_tile.isHovered(mouse_pos, camera):
          return grid_tile
    return None


  # drawing enviroment - walls + grid made of tiles
  #  
  def draw(self, renderer: Renderer) -> None:

    surface = renderer.getSurface()

    for row in self._grid_tiles:

      for grid_tile in row:

        if(grid_tile.isVisible(renderer)):
          grid_tile.draw(surface)             # drawing tile itself

    # only bottom and right edges are drawn to save resources, thus n + 1 lines must be drawn

    for y in range(len(self._grid_nodes)):

      for x in range(len(self._grid_nodes[y])):

        grid_node = self._grid_nodes[y][x]

        if x + 1 < len(self._grid_nodes[y]):

          right_grid_node = self._grid_nodes[y][x + 1]                                  # position to draw line
          pygame.draw.line(surface, TAIL_EDGE_COLOR, grid_node, right_grid_node)

        if y + 1 < len(self._grid_nodes):

          bottom_grid_node = self._grid_nodes[y + 1][x]                                # position to draw line
          pygame.draw.line(surface, TAIL_EDGE_COLOR, grid_node, bottom_grid_node)

    # Drawing outside walls
    for wall in self._walls:
      wall.draw(surface)










## [TODO] Init cache full walls less math
class Wall:
  def __init__(self, Grid_Node_1 : np.ndarray[int], Grid_Node_2 : np.ndarray[int], height : int):
    self._Grid_Node_1 = Grid_Node_1
    self._Grid_Node_2 = Grid_Node_2
    self._height = height


  def draw(self, surface: pygame.Surface) -> None:
    x_1, y_1 = self._Grid_Node_1
    x_2, y_2 = self._Grid_Node_2

    points = (
      (x_1, y_1),
      (x_2, y_2),
      (x_2, y_2 - self._height),
      (x_1, y_1 - self._height)
    )

    pygame.draw.polygon(surface, WALL_COLOR, points)
    pygame.draw.polygon(surface, WALL_EDGE_COLOR, points, 1) 
