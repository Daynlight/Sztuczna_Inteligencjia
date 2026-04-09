import numpy as np
import os

from Classes.Core.Renderer.Renderer import Renderer
from Classes.Core.Grid.Grid import Grid
from Classes.Core.Renderer.Light import Light

from Classes.Core.Object.Object import Object
from Classes.Objects.Static.Table import Table
from Classes.Objects.Static.GroupTable import GroupTable
from Classes.Objects.Static.Counter import Counter
from Classes.Objects.Static.Chair import Chair
from Classes.Objects.Beings.Client import Client
from Classes.Objects.Beings.Waiter import Waiter
from Classes.Objects.Beings.Cook import Cook
from Classes.Core.Object.Wall import WallObject

from conf import TILE_SIZE, GRID_X, GRID_Y, MARGIN_HORIZONTAL, MARGIN_VERTICAL, WINDOW_HEIGHT, WINDOW_WIDTH, TITLE, BACKGROUND_COLOR

# AI stuff
class Model:
  def __init__(self):
    self._running: bool = True
    self._initialized: bool = False
    self._collisions_objects: np.ndarray[Object] = np.array([], dtype=Object)
    self._render_objects: np.ndarray[Object] = np.array([], dtype=Object)
    self._renderer: Renderer = None
    self._grid: Grid = None


  def __del__(self):
    if(self._renderer):
      del self._renderer
    if(self._grid):
      del self._grid


  def _initModel(self) -> None:
    if(self._initialized == True): return

    ## Init Grid
    self._grid: Grid = Grid(GRID_X, GRID_Y , TILE_SIZE, MARGIN_HORIZONTAL, MARGIN_VERTICAL)

    ## Init Lights
    self._light: np.ndarray[Light] = np.array([
      Light([self._grid._grid_tiles[0][0].getRenderPos()[0],                   self._grid._grid_tiles[0][0].getRenderPos()[1],                   90], [255/255, 200/255, 160/255], 0.35),
      Light([self._grid._grid_tiles[GRID_X - 1][GRID_Y - 1].getRenderPos()[0], self._grid._grid_tiles[GRID_X - 1][GRID_Y - 1].getRenderPos()[1], 90], [255/255, 200/255, 160/255], 0.35),
      Light([self._grid._grid_tiles[0][GRID_Y - 1].getRenderPos()[0],          self._grid._grid_tiles[0][GRID_Y - 1].getRenderPos()[1],          90], [255/255, 200/255, 160/255], 0.35),
      Light([self._grid._grid_tiles[GRID_X - 1][0].getRenderPos()[0],          self._grid._grid_tiles[GRID_X - 1][0].getRenderPos()[1],          90], [255/255, 200/255, 160/255], 0.35),
      Light([self._grid._grid_tiles[5][5].getRenderPos()[0],   self._grid._grid_tiles[5][5].getRenderPos()[1],   90], [255/255, 200/255, 160/255], 0.4),
      Light([self._grid._grid_tiles[15][15].getRenderPos()[0], self._grid._grid_tiles[15][15].getRenderPos()[1], 90], [255/255, 200/255, 160/255], 0.4),
      Light([self._grid._grid_tiles[5][15].getRenderPos()[0],  self._grid._grid_tiles[5][15].getRenderPos()[1],  90], [255/255, 200/255, 160/255], 0.4),
      Light([self._grid._grid_tiles[15][5].getRenderPos()[0],  self._grid._grid_tiles[15][5].getRenderPos()[1],  90], [255/255, 200/255, 160/255], 0.4)
    ], dtype=Light)

    ## Init Walls
    self._walls = np.array([
      WallObject(texture_path="Handmade/Static/Wall/Wall2.png", normals_texture_path="Handmade/Static/Wall/Wall2_Normals.png", position=[0, 0], direction=[0, 1], numbers=2),
      WallObject(texture_path="Handmade/Static/Wall/Wall1.png", position=[0, 2], direction=[0, 1], numbers=GRID_Y - 2),
      WallObject(texture_path="Handmade/Static/Wall/Wall2_rotated.png", normals_texture_path="Handmade/Static/Wall/Wall2_Normals_rotated.png", position=[0, 0], direction=[1, 0], numbers=4),
      WallObject(texture_path="Handmade/Static/Wall/Wall1_rotated.png", position=[4, 0], direction=[1, 0], numbers=GRID_X - 4),
    ], dtype=WallObject)

    ## Init Objects
    self._waiter: Waiter = Waiter([6, 6], [TILE_SIZE/2, TILE_SIZE/2 - TILE_SIZE])
    self._cook: Cook = Cook([0, 0], [TILE_SIZE/2, TILE_SIZE/2 - TILE_SIZE])

    self._tables: np.ndarray[Table] = np.array([
        Table([3,10], render_order=2),
        Table([3,9]),
        Table([8,3]),
        Table([7,6]),
        Table([10,12]),
        Table([11,12]),
        Table([0, 6]),
        Table([0, 7]),
        Table([1, 6]),
        Table([1, 7]),
    ], dtype=Table)

    self._chairs: np.ndarray[Chair] = np.array([
        Chair([3,11]),
        Chair([3,8]),
        Chair([4,10]),
        Chair([8,4]),
        Chair([9,3]),
        Chair([7,5]),
        Chair([10,13]),
        Chair([11,13]),
        Chair([12,12]),
        Chair([10,11]),
        Chair([11,11]),
        Chair([9,12]),
        Chair([7,3]),
        Chair([0, 5]),
        Chair([1, 5]),
        Chair([2, 6], "souteast"),
        Chair([2, 7], "souteast"),
        Chair([0, 8], "southwest"),
        Chair([1, 8], "southwest"),
    ], dtype=Chair)

    self._counters: np.ndarray[Counter] = np.array([
      Counter([0,2]),
      Counter([1,2]),
      Counter([2,2]),
      Counter([3,2]),
      Counter([4,2]),
      Counter([4,1], render_order=0),
      Counter([4,0]),
    ], dtype=Counter)

    self._groupTable: np.ndarray[GroupTable] = np.array([
      GroupTable("Stolik nr 1", self._tables[0])
    ], dtype=GroupTable)


    self._clients: np.ndarray[Client] = np.array([
      Client([1, 1], [TILE_SIZE/2, TILE_SIZE/2]),
      Client([1, 1], [TILE_SIZE/2, TILE_SIZE/2]),
      Client([1, 1], [TILE_SIZE/2, TILE_SIZE/2]),
    ], dtype=Client)

    ## Add chairs
    self._tables[2].addChair(self._chairs[4])
    self._tables[1].addChair(self._chairs[1])
    self._tables[0].addChair(self._chairs[2])
    self._tables[0].addChair(self._chairs[0])
    self._tables[2].addChair(self._chairs[3])	
    self._tables[2].addChair(self._chairs[12])
    self._tables[3].addChair(self._chairs[5])
    self._tables[4].addChair(self._chairs[6])
    self._tables[4].addChair(self._chairs[9])
    self._tables[4].addChair(self._chairs[11])
    self._tables[5].addChair(self._chairs[7])
    self._tables[5].addChair(self._chairs[8])
    

    #self._tables[1].removeChair(self._chairs[2])
    #self._tables[2].addChair(self._chairs[2])

    ## Grouping tables
    self._groupTable[0].addTable(self._tables[1])

    ## Assign clients to tables
    self._clients[0].assignTable(self._tables[0])
    self._clients[1].assignTable(self._tables[1])
    self._clients[2].assignTable(self._tables[2])

    ## Client Orders
    self._clients[0].makeOrder("taco")
    self._clients[1].makeOrder("fried_egg")
    self._clients[2].makeOrder("pancake")

    ## Receive Orders from clients by waiter
    self._waiter.receiveOrder(self._clients[0])
    self._waiter.receiveOrder(self._clients[1])

    ## Receive Orders from waiter to cook
    self._cook.takeOrderFromWaiter(self._waiter)
    self._cook.makeFood()

    ## Take food from cook by waiter
    self._waiter.takeFood(self._cook)
    self._waiter.completeOrder()

    # Create List of Objects to Render
    self._render_objects: np.ndarray[Object] = np.array([ self._waiter, self._cook, *self._clients, *self._tables, *self._chairs, *self._counters ], dtype=Object)
    
    # Create List of Collisions for path finding
    self._collisions_objects: np.ndarray[Object] = np.array([ *self._tables, *self._chairs, *self._counters ], dtype=Object)

    # Precompute Lights
    self._grid.precomputeLight(self._light)
    for el in self._render_objects:
      el.precomputeLight(self._grid, self._light)
    for el in self._walls:
      el.precomputeLight(self._grid, self._light)
      
    self._initialized: bool = True

  def _initRenderer(self) -> None:
    if(self._renderer == None): self._renderer: Renderer = Renderer(TITLE, WINDOW_WIDTH, WINDOW_HEIGHT)


  def isRunning(self) -> bool:
    if(self._renderer): self._running: bool = self._renderer.getRunning()
    return self._running


  def modelIteration(self, acceleration: float = 1.0) -> None:
    if(self._initialized == False): self._initModel()
    if(self._renderer == None): self._initRenderer()

    mouse_pos: np.ndarray[int] = self._renderer.getMouse()
    if(mouse_pos != None): 
      hovered_tile: np.ndarray[int] = self._grid.get_hovered_tile(mouse_pos, self._renderer.getCamera())

      if hovered_tile:
        self._waiter.goTo(hovered_tile, self._collisions_objects)
    
    self._waiter.makeStep(self._renderer.getDeltaTime(), acceleration)


  def _renderOrder(self) -> None:
    distances: np.ndarray[float] = np.array([np.dot(e.getPosition(), e.getPosition()) for e in self._render_objects], dtype=float)
    orders: np.ndarray[int] = np.array([e.getRenderOrder() for e in self._render_objects], dtype=int)

    indices = np.lexsort((orders, distances))
    self._render_objects: np.ndarray[Object] = self._render_objects[indices]
    

  def renderFrame(self) -> None:
    if(self._initialized == False): self._initModel()
    if(self._renderer == None): self._initRenderer()

    self._renderOrder()

    self._renderer.backgroundColor(BACKGROUND_COLOR)
    self._grid.draw(self._renderer, self._light)

    for el in self._walls:
      el.render(self._renderer.getSurface(), self._grid, self._renderer, self._light)

    for el in self._render_objects:
      el.render(self._renderer.getSurface(), self._grid, self._renderer, self._light)


    self._renderer.renderFrame()
