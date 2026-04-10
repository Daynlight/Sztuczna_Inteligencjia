import pygame
import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from Classes.Core.Renderer.Renderer import Camera, Renderer

import Classes.Objects.TextureManager as TextureManager

from conf import TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH, BEING_MOVEMENT_DIRECTIONS


texture_lock = threading.Lock()

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
    self._texture = TextureManager.TILE_TEXTURE
    self._lit_texture: pygame.Surface = None


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
  

  def precomputeLight(self, lights: list):
      render_pos = self.getRenderPos()
      with texture_lock:  
          self._lit_texture = self._texture.getLitTexture(render_pos, lights)


  def draw(self, surface: pygame.Surface, lights: list) -> None:
    render_pos = self.getRenderPos()
    if(self._lit_texture == None):
      self._lit_texture = self._texture.getLitTexture(render_pos, lights)
      
    surface.blit(self._lit_texture, render_pos)


  def isVisible(self, renderer: Renderer) -> bool:
    render_pos = self.getRenderPos()
    camera: Camera = renderer.getCamera()
    viewport = [render_pos[0] - camera.getRect().x, render_pos[1] - camera.getRect().y]

    if(viewport[0] + TILE_SIZE * 2 < 0): return False
    if(viewport[1] + TILE_SIZE * 2 < 0): return False
    if(viewport[0] > WINDOW_WIDTH): return False
    if(viewport[1] > WINDOW_HEIGHT): return False

    return True










class Grid:
  def __init__(self, size_x: int, size_y: int, grid_tile_size : int, margin_horizontal : int, margin_vertical: int):
    self._size: np.ndarray[int] = np.array([size_x, size_y], dtype=int)
    self._grid_tile_size: int = grid_tile_size
    self._margins: np.ndarray[int] = np.array([margin_horizontal, margin_vertical], dtype=int)
    self._grid_nodes: np.ndarray[np.ndarray[int]] = None
    self._grid_tiles: np.ndarray[np.ndarray[Grid_Tile]] = None
    self._graph = {}

    self._generateGridNodes()
    self._generateGridTails()


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


  def precomputeLight(self, lights: list) -> None:
    tasks = []
    all_tiles = [self._grid_tiles[x][y] for y in range(self._size[1]) for x in range(self._size[0])]

    with ThreadPoolExecutor() as executor:
      for tile in all_tiles:
        tasks.append(executor.submit(tile.precomputeLight, lights))
      for future in as_completed(tasks):
        future.result()


  def get_hovered_tile(self, mouse_pos: np.ndarray[int], camera : Camera) -> Grid_Tile:
    # method to get the tile hovered by mouse, currently used to make the waiter go to selected tile

    for row in self._grid_tiles:
      for grid_tile in row:
        if grid_tile.isHovered(mouse_pos, camera):
          return grid_tile
    return None
  

  def _graphCheckForCollisions(self, collisions, new_node) -> bool:
    collision = any(np.array_equal(el.getPosition(), new_node) for el in collisions)
    return collision

  
  def _graphCheckForMapEdges(self, new_node)  -> bool:
    collision = new_node[0] >= 0 and new_node[1] >= 0 and new_node[0] < self._size[0] and new_node[1] < self._size[1]
    return collision


  def _graphCheckForWalls(self, current_position, new_node, walls) -> bool:
    collision = False

    # check each wall
    for el in walls:
      # getting two lists of restricted movement (going through wall)
      restricted_movement = el.getMovementRestriction()
      if restricted_movement is None:
        continue
      
      # first check if current pos in first list
      in_restricted_area = False
      for el in restricted_movement[0]:
        if np.array_equal(el, np.array(current_position, dtype=int)):
          in_restricted_area = True
          break
        
      if in_restricted_area:
        for el in restricted_movement[1]:
          if np.array_equal(el, np.array(new_node, dtype=int)):
            collision = True
            break
      
      # second check (opposite direction)
      in_restricted_area = False
      for el in restricted_movement[1]:
        if np.array_equal(el, np.array(current_position, dtype=int)):
          in_restricted_area = True
          break
        
      if in_restricted_area:
        for el in restricted_movement[0]:
          if np.array_equal(el, np.array(new_node, dtype=int)):
            collision = True
            break

    return collision


  def generateNeighborsGraph(self, collisions, walls) -> None:
    for y in range(0, self._size[1]):
      for x in range(0, self._size[0]):
        connections = []
        for d in BEING_MOVEMENT_DIRECTIONS:
          new_node = np.array([x, y], dtype=int) + d

          collision = not self._graphCheckForMapEdges(new_node)
          if(not collision): collision = self._graphCheckForCollisions(collisions, new_node)
          if(not collision): collision = self._graphCheckForWalls(np.array([x, y], dtype=int), new_node, walls)
          
          if(not collision): connections.append((int(new_node[0]), int(new_node[1])))
          
        self._graph[(x, y)] = connections


  def getNeighbors(self, position) -> list[np.ndarray[int]]:
    return self._graph[tuple(position)]


  def draw(self, renderer: Renderer, lights: list) -> None:
    surface = renderer.getSurface()         
    for row in self._grid_tiles:

      for grid_tile in row:

        if(grid_tile.isVisible(renderer)):
          grid_tile.draw(surface, lights)
