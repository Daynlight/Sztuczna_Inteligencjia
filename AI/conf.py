import os
import pygame









TILE_SIZE: int = 40
WAITER_VELOCITY: int = 10

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

MARGIN_HORIZONTAL = 130
MARGIN_VERTICAL = 130

GRID_X = 15    #grids
GRID_Y = 15   #grids

WORLD_WIDTH = GRID_X * TILE_SIZE * 2 + 2 * MARGIN_HORIZONTAL
WORLD_HEIGHT = GRID_Y * TILE_SIZE + 2 * MARGIN_VERTICAL

CAMERA_SPEED = 300

TAIL_COLOR = [204, 169, 149]
TAIL_EDGE_COLOR = [156, 128, 112]
WALL_COLOR = [245, 160, 95]
WALL_EDGE_COLOR = [0, 0, 0]

BACKGROUND_COLOR = [41, 40, 40]
WALL_HEIGHT = 100
TITLE = "Waiter AI"

PATH_TO_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Assets")
TEXTURE_ERROR_COLORS = [(255, 0, 220), (1, 0, 1)]

ERROR_TEXTURE = pygame.Surface((64, 64))
for y in range(8):
  for x in range(8):
    rect = pygame.Rect(8 * x, 8 * y, 8, 8)
    color = TEXTURE_ERROR_COLORS[(x + y) % 2]
    ERROR_TEXTURE.fill(color, rect)