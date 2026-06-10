import pygame
import numpy as np
import os
from enum import Enum, auto







 

DEBUG = False
DYNAMIC_LIGHTS = True

TILE_SIZE: int = 40
WAITER_VELOCITY: int = 6

PATH_TO_ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PATH_TO_MODEL_DIR = os.path.join(PATH_TO_ROOT_DIR, "Models")
PATH_TO_DATASET_DIR = os.path.join(PATH_TO_ROOT_DIR, "Dataset")

PATH_TO_NN_DATASET = os.path.join(PATH_TO_DATASET_DIR, "NN_dataset.txt")
PATH_TO_DT_DATASET = os.path.join(PATH_TO_DATASET_DIR, "DT_dataset.txt")
PATH_TO_NN_WAITER_MODEL = os.path.join(PATH_TO_MODEL_DIR, "waiter_model.pth")
PATH_TO_DECISION_TREE = os.path.join(PATH_TO_MODEL_DIR, "decision_tree.txt")

BEING_MOVEMENT_DIRECTIONS = [
  np.array([0, -1]),  # north
  np.array([1, 0]),   # east
  np.array([0, 1]),   # south
  np.array([-1, 0])   # west
]

class PATH_SEARCH_VARIANTS(Enum):
  BFS = auto()
  A_STAR = auto()

PATH_SEARCH_VARIANT = PATH_SEARCH_VARIANTS.A_STAR
SEARCH_VISUALIZATION = False
SEARCH_HZ = 480

class LEARN_VARIANTS(Enum):
  NEURAL_NETWORK = auto()
  DECISION_TREE = auto()

LEARN_VARIANT = LEARN_VARIANTS.NEURAL_NETWORK

BEING_DEFAULT_MOVE_COST = 1
BEING_DEFAULT_ROTATE_COST = 0.1

FIXED_UPDATE_HZ = 60
FPS_SAMPLES = 10

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



# GENETIC ALGORITHM PARAMS
GENETIC_SEATING_ARRANGEMENT = False

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

