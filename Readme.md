# Projekt Sztuczna Inteligencjia
## Automatyczny kelner
Zadaniem automatycznego kelnera jest przyjmowanie zamówień i dostarczanie posiłków klientom. Agent
rozpoznaje przygotowany w kuchni posiłek, a następnie na postawie historii zamówień wybiera stolik, do
którego należy go dostarczyć.



## TOC
- [Projekt Sztuczna Inteligencjia](#projekt-sztuczna-inteligencjia)
  - [Automatyczny kelner](#automatyczny-kelner)
  - [TOC](#toc)
  - [Installation](#installation)
  - [Architecture](#architecture)
  - [Classes](#classes)
    - [Window](#window)
    - [Object](#object)
    - [Grid](#grid)
    - [Tile](#tile)
    - [World](#world)
    - [Camera](#camera)
    - [Table](#table)
  - [Files and Function](#files-and-function)
    - [main](#main)
    - [learn](#learn)
    - [init scene](#init-scene)
    - [conf](#conf)
  - [Prerequisites](#prerequisites)
  - [TODO:](#todo)



## Installation
1. Install python and git
    ```bash
    sudo apt install python3 git
    ```
2. Clone repository
    ```bash
    git clone https://git.wmi.amu.edu.pl/s500044/Sztuczna_Inteligencja_Projekt
    cd Sztuczna_Inteligencja_Projekt
    ```
3. Create env and install requirements
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
4. Run program in visual mode
    ```bash
    cd AI
    python3 main.py 
    ```
5. Run in learning mode
    ```bash
    cd AI
    python3 learn.py
    ```



## Architecture
1. Program contains two parts 
   1. learn used only for model learning.
   2. main used only for visualization.
   3. rest of code like environment, scene and others are ran independent from this functions.
2. Movement
   1. Kelner can move to destination via ```goTo()```.
   2. After ```goTo()``` Kelner creates path with proper algorithm.
   3. When path is done than Kelner makes moves with ```makeMove()```.
   4. Klener makes moves with specified speed using ```deltaTime``` from window. 
   5. In learning mode we don't use delta time for faster learning process.



## Classes
### Window
Used for creating window with pygame and getting window inputs
  * **def __init__(self, title: str, width: int = 800, height: int = 600)**: default class constructor.
  * **def __del__(self)**: default class destructor.
  * **def CreateWindow(self, title: str, width: int = 800, height: int = 600)**: creation of window.
  * **def PoolEvents(self)**: getting window events like **quit**, **mouse events**. 
  * **def SwapBuffer(self)**: updating window.
  * **def loop(self, render: Callable[[pygame.Surface], None])**: main program loop.

### Object
Used for object on scene
  * **def __init__(self, name, texture_path, position: np.array, velocity: float, size: np.array)**: default class constructor.
  * **def __del__(self)**: default class destructor.
  * **def setPosition(self, position: np.array)**: setting position on grid.
  * **def setSize(self, size: np.array)**: settings size on grid.
  * **def setTexture(self, texture_path, size: np.array)**: setting texture on grid.
  * **def goTo(self, position: np.array)**: giving command to go somewhere.
  * **def generatePath(self, current_position: np.array, position: np.array, depth = 20)**: creating path to destination.
  * **def makeStep(self, deltaTime: float)**: making single step.
  * **def render(self, window: pygame.Surface)**: render object.
* Additional ```objectMap = {}``` used for iteration and fast update of object.

### Grid
Creates a 2D isometric grid of objects from Tile Class
  * **def __init__(self, size_x: int, size_y: int, tile_size, margin_top, margin_left)**: default class constructor.
  * **def __del__(self)**: default class destructor.
  * **def get_hovered_tile(self, mouse_pos, camera : Camera)**: Returns the tile that is currently hovered by mouse
  * **def draw(self, surface):**: draws grid on given surface

### Tile
Creates a diamond rhombus with diagonals a x 2a
  * **def __init__(self, center_x, center_y, a, isometric_x, isometric_y)**: default class constructor.
  * **def __del__(self)**: default class destructor.
  * **def isHovered(self, mouse_pos, camera : Camera):**: Returns True if given tile is hovered by a mouse; otherwise returns False
  * **def draw(self, target_surface):**: draws tile on given surface

### World
Creates game's world based pn pygame.Surface
  * **def __init__(self, width : int, height : int)**: default class constructor
  * **def draw(self)**: draws world surface

### Camera
Creates camera for viewing only a part of the world's surface
  * **def __init__(self, width: int, height: int, center_x_pos, center_y_pos)**: default class constructor
  * **def update(self)**: updates camera's position
### Table
Inherits from Object
  * **def __init__(self, name, position, active=False)**: default class constructor

## Files and Function
### main
visual app runner

### learn
non visual learning process

### init scene
initialization of objects on scene

### conf
configuration stuff like widnow size, world_size etc.


## Prerequisites
- **pygame**: for rendering.
- **numpy**: for mathematical operations.



## TODO:

<details open>
<summary>Task 1</summary>

[env](docs/lab2%20environment-task.pdf) 11.03.2026
- [x] Init pygame and Create Window (Daniel)
- [x] Basic Object class and render (Daniel)
- [x] Move to isometric space. (Martyna)
- [x] Grid base world. (Martyna)
- [x] Camera Movement. (Martyna)
- [ ] Inherit Classes from Object, separation and storage in variable base on type.
- [ ] Add path finding sth simple for now BFS or A* with delta time.
- [ ] Add own custom assets and level design.
- [ ] Animations.

</details>