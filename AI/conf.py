import os
import pygame


TILE_SIZE: int = 40
WAITER_VELOCITY: int = 10

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

MARGIN_HORIZONTAL = 130 # Marhing left
MARGIN_VERTICAL = 130 # Margin top

GRID_X = 20    #grids
GRID_Y = 20   #grids

WORLD_WIDTH = GRID_X * TILE_SIZE * 2 + 2 * MARGIN_HORIZONTAL          # World width is calulated so the world will be centered
WORLD_HEIGHT = GRID_Y * TILE_SIZE + 2 * MARGIN_VERTICAL               # World height is calulated so the world will be centered

CAMERA_SPEED = 300

TAIL_EDGE_COLOR = [156, 128, 112]
WALL_COLOR = [245, 160, 95]
WALL_EDGE_COLOR = [0, 0, 0]

BACKGROUND_COLOR = [41, 40, 40]
WALL_HEIGHT = 100

TITLE = "Waiter AI"                     # Title of the window 

PATH_TO_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Assets")

# Background color when texture cannot be loaded
TEXTURE_ERROR_COLORS = [(255, 0, 220), (1, 0, 1)]

ERROR_TEXTURE = pygame.Surface((64, 64))
for y in range(8):
  for x in range(8):
    rect = pygame.Rect(8 * x, 8 * y, 8, 8)
    color = TEXTURE_ERROR_COLORS[(x + y) % 2]
    ERROR_TEXTURE.fill(color, rect)