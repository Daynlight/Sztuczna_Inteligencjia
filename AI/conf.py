import pygame
import numpy as np









DEBUG = False
DYNAMIC_LIGHTS = True

TILE_SIZE: int = 40
WAITER_VELOCITY: int = 6

BEING_MOVEMENT_DIRECTIONS = [
  np.array([0, -1]),  # north
  np.array([1, 0]),   # east
  np.array([0, 1]),   # south
  np.array([-1, 0])   # west
]

BEING_DEFAULT_MOVE_COST = 1
BEING_DEFAULT_ROTATE_COST = 0.1


# GENETIC ALGORITHM PARAMS
GENETIC_SEATING_ARRANGEMENT = True

# tables and chairs must have the same length !11!!!
TABLE_ARRANGEMENT = np.array([2, 1, 2, 1, 2, 3, 2])
CHAIR_ARRANGEMENT = np.array([6, 6, 4, 4, 6, 8, 6])

OBSTACLE_ARRAY = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
])


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

# Background color when texture cannot be loaded
TEXTURE_ERROR_COLORS = [(255, 0, 220), (1, 0, 1)]

ERROR_TEXTURE = pygame.Surface((64, 64))
for y in range(8):
  for x in range(8):
    rect = pygame.Rect(8 * x, 8 * y, 8, 8)
    color = TEXTURE_ERROR_COLORS[(x + y) % 2]
    ERROR_TEXTURE.fill(color, rect)
