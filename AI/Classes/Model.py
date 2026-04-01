import numpy as np

from Classes.Renderer.Renderer import Renderer
from Classes.Grid.Grid import Grid

from Classes.Objects.Object import Object
from Classes.Objects.Static.Table import Table
from Classes.Objects.Static.GroupTable import GroupTable
from Classes.Objects.Static.Counter import Counter
from Classes.Objects.Static.Chair import Chair
from Classes.Objects.Beings.Client import Client
from Classes.Objects.Beings.Waiter import Waiter
from Classes.Objects.Beings.Cook import Cook

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

    ## Init Objects
    self._waiter: Waiter = Waiter([1, 1], [TILE_SIZE/2, TILE_SIZE/2])
    self._cook: Cook = Cook([0, 5], [TILE_SIZE/2, TILE_SIZE/2])

    self._tables: np.ndarray[Table] = np.array([
        Table([3,10], render_order=2),
        Table([3,9]),
        Table([8,3]),
        Table([7,6]),
        Table([10,12]),
        Table([11,12])
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
        Chair([7,3])
    ], dtype=Chair)

    self._counters: np.ndarray[Counter] = np.array([
      Counter([0,4]),
      Counter([1,4]),
      Counter([1,5]),
      Counter([1,6]),
      Counter([1,7]),
      Counter([0,7], render_order=0),
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
    self._grid.draw(self._renderer)

    for el in self._render_objects:
      el.render(self._renderer.getSurface(), self._grid, self._renderer)

    self._renderer.renderFrame()
