import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

from Classes.Core.Renderer.Renderer import Renderer
from Classes.Core.Grid.Grid import Grid
from Classes.Core.Renderer.Light import Light
from Classes.Core.Object.Object import Object

import Classes.Objects.TextureManager as TextureManager
from Classes.Objects.Static.Table import Table
from Classes.Objects.Static.GroupTable import GroupTable
from Classes.Objects.Static.Counter import Counter
from Classes.Objects.Static.Chair import Chair
from Classes.Objects.Static.Couch import Couch
from Classes.Objects.Beings.Client import Client
from Classes.Objects.Beings.Waiter import Waiter
from Classes.Objects.Beings.Cook import Cook
from Classes.Core.Object.Wall import Wall
from Classes.Objects.Static.Sink import Sink
from Classes.Objects.Static.Fridge import Fridge
from Classes.Objects.Static.Stove import Stove
from Classes.Objects.Static.Dishwasher import Dishwasher
from Classes.Objects.Static.OrderList import OrderList
from Classes.Objects.Static.Flower import Flower

from conf import TILE_SIZE, GRID_X, GRID_Y, MARGIN_HORIZONTAL, MARGIN_VERTICAL, WINDOW_HEIGHT, WINDOW_WIDTH, TITLE, BACKGROUND_COLOR









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


  def precomputeLight(self):
    tasks = []

    with ThreadPoolExecutor() as executor:
      tasks.append(executor.submit(self._grid.precomputeLight, self._light))
      for el in self._render_objects:
        tasks.append(executor.submit(el.precomputeLight, self._grid, self._light))
      for el in self._walls:
        tasks.append(executor.submit(el.precomputeLight, self._grid, self._light))
      for future in as_completed(tasks):
        future.result()


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
      Light([self._grid._grid_tiles[15][5].getRenderPos()[0],  self._grid._grid_tiles[15][5].getRenderPos()[1],  90], [255/255, 200/255, 160/255], 0.4),

      Light([self._grid._grid_tiles[17][2].getRenderPos()[0],  self._grid._grid_tiles[19][0].getRenderPos()[1],  90], [255/255, 200/255, 160/255], 0.4),
      Light([self._grid._grid_tiles[17][3].getRenderPos()[0],  self._grid._grid_tiles[19][1].getRenderPos()[1],  90], [255/255, 200/255, 160/255], 0.4)
    ], dtype=Light)

    ## Init Walls
    self._walls = np.array([
      # Kitchen
      Wall(texture=TextureManager.WALL2_TEXTURE, position=[0, 0], direction=[0, 1], numbers=4),
      Wall(texture=TextureManager.WALL2_ROTATED_TEXTURE, position=[0, 0], direction=[1, 0], numbers=4),
      Wall(texture=TextureManager.WALL1_2_TEXTURE, position=[0, 4], direction=[0, 1], numbers=1),
      Wall(texture=TextureManager.WALL1_2_ROTATED_TEXTURE, position=[4, 0], direction=[1, 0], numbers=1),
      
      # Main Room
      Wall(texture=TextureManager.WALL1_TEXTURE, position=[0, 5], direction=[0, 1], numbers=GRID_Y - 5),
      Wall(texture=TextureManager.WALL1_ROTATED_TEXTURE, position=[5, 0], direction=[1, 0], numbers=GRID_X - 5),
      
      # Entrance
      Wall(texture=TextureManager.WALL1_TEXTURE, position=[15, 0], direction=[0, 1], numbers=4),

      Wall(texture=TextureManager.WALL1_TEXTURE, position=[10, 0], direction=[0, 1], numbers=4)
    ], dtype=Wall)

    self.order_list: Object = OrderList(position=[5, 0])

    ## Init Objects
    self._waiter: Waiter = Waiter([6, 6], [TILE_SIZE/2, TILE_SIZE/2 - TILE_SIZE])
    self._cook: Cook = Cook([2, 1], offset=[TILE_SIZE/2, TILE_SIZE/2 - TILE_SIZE])

    self._tables: np.ndarray[Table] = np.array([
        Table([3,10], render_order=2),

        Table([12,6]),
        Table([12,7]),
        Table([13,6]),
        Table([13,7]),

        Table([12,11]),
        Table([13,11]),


        Table([0, 8]),
        Table([0, 9]),
        Table([1, 8]),
        Table([1, 9]),

        Table([0, 15]),
        Table([0, 16]),
        Table([1, 15]),
        Table([1, 16]),

        Table([17, 2]),
        Table([17, 3]),
        Table([18, 2]),
        Table([18, 3]),

        
        Table([12, 2]),
        Table([12, 3]),
        Table([13, 2]),
        Table([13, 3]),

    ], dtype=Table)

    self._chairs: np.ndarray[Chair] = np.array([
        Chair([3,11]),
        Chair([3,8]),
        Chair([4,10]),

        Chair([11,6], "northwest"),
        Chair([11,7], "northwest"),
        Chair([14,6], "southwest"),
        Chair([14,7], "southwest"),


        Chair([12,12], "southeast"),
        Chair([13,12], "southeast"),
        Chair([14,11], "southeast"),
        Chair([12,10], "northeast"),
        Chair([13,10], "northeast"),
        Chair([11,11], "northwest"),

        
        Chair([0, 7]),
        Chair([1, 7]),
        Chair([2, 8], "souteast"),
        Chair([2, 9], "souteast"),
        Chair([0, 10], "southwest"),
        Chair([1, 10], "southwest"),

        Chair([0, 14]),
        Chair([1, 14]),
        Chair([0, 17], "southwest"),
        Chair([1, 17], "southwest")
    ], dtype=Chair)

    self._couches: np.ndarray[Couch] = np.array([

        Couch([16,1], "northwest"),
        Couch([16,2], "northwest"),
        Couch([16,3], "northwest"),
        Couch([16,0], "middle"),
        Couch([17,0], "northeast"),
        Couch([18,0], "northeast"),
        Couch([19,0], "northeast"),

        Couch([11,1], "northwest"),
        Couch([11,2], "northwest"),
        Couch([11,3], "northwest"),
        Couch([11,0], "middle"),
        Couch([12,0], "northeast"),
        Couch([13,0], "northeast"),
        Couch([14,0], "northeast"),

    ], dtype=Couch)

    self._counters: np.ndarray[Counter] = np.array([
      Counter([4,0]),
      Counter([4,1]),
      Counter([4,2]),
      Counter([4,3]),
      Counter([4,4]),
      Counter([3,4]),
      Counter([2,4], render_order=0),
      Counter([1,4]),
    ], dtype=Counter)

    self._sinks: np.ndarray[Sink] = np.array([
      Sink([0,1]),
    ], dtype=Sink)

    self._fridges: np.ndarray[Fridge] = np.array([
      Fridge([0,0]),
    ], dtype=Fridge)

    self._stoves: np.ndarray[Stove] = np.array([
      Stove([0,2]),
    ], dtype=Stove)

    self._dishwashers: np.ndarray[Dishwasher] = np.array([
      Dishwasher([3,0]),
    ], dtype=Dishwasher)


    self._flowers: np.ndarray[Flower] = np.array([
      Flower([0,12]),
      Flower([6,0]),
    ], dtype=Flower)

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
    self._render_objects: list[Object] = [ self._waiter, self._cook, *self._clients, *self._couches , self.order_list, *self._tables, *self._chairs, 
                                            *self._counters, *self._sinks, *self._fridges,*self._dishwashers ,*self._flowers, *self._stoves ]
    for el in self._walls:
      objects = el.getObjects()
      for ela in objects:
        self._render_objects.append(ela)
    self._render_objects = np.array(self._render_objects, dtype=Object)
    
    
    # Create List of Collisions for path finding
    self._collisions_objects: np.ndarray[Object] = np.array([ *self._tables, *self._chairs, *self._counters, *self._sinks, *self._flowers ], dtype=Object)

    self.precomputeLight()
      
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
        self._waiter.goTo(hovered_tile, self._collisions_objects, self._walls)
    
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

    # for el in self._walls:
    #   el.render(self._renderer.getSurface(), self._grid, self._renderer, self._light)

    for el in self._render_objects:
      el.render(self._renderer.getSurface(), self._grid, self._renderer, self._light)


    self._renderer.renderFrame()
