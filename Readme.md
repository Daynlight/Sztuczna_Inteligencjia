# Projekt Sztuczna Inteligencjia
## Automatyczny kelner
Zadaniem automatycznego kelnera jest przyjmowanie zamówień i dostarczanie posiłków klientom. Agent
rozpoznaje przygotowany w kuchni posiłek, a następnie na postawie historii zamówień wybiera stolik, do
którego należy go dostarczyć.



## TOC
- [Automatyczny kelner](#automatyczny-kelner)
- [TOC](#toc)
- [Installation](#installation)
- [Architecture](#architecture)
- [Classes](#classes)
  - [Window](#window)
  - [Object](#object)
- [Files and Function](#files-and-function)
  - [main](#main)
  - [learn](#learn)
  - [init scene](#init-scene)
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



## Files and Function
### main
visual app runner

### learn
non visual learning process

### init scene
initialization of objects on scene



## Prerequisites
- **pygame**: for rendering.
- **numpy**: for mathematical operations.



## TODO:
- [x] [env](docs/lab2%20environment-task.pdf) 11.03.2026
- [ ] Add path finding sth simple for now BFS or DFS.
- [ ] Add own custom assets.
- [ ] Move to isometric space.
- [ ] Add simple back propagation with neural network.
