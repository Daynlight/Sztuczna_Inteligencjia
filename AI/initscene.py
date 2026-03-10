from Classes.Table import Table
from Classes.Chair import Chair
from Classes.Beings.Client import Client
from Classes.Beings.Waiter import Waiter
from Classes.Beings.Cook import Cook
from Classes.Object import Object
from Classes.Grid import Wall, Node
from conf import movementSpeed, gridSize



kelner = Waiter("kelner", [1, 1], [gridSize/2, gridSize/2])
kucharz = Cook("kucharz", [0, 5], [gridSize/2, gridSize/2])

stoliki = [
    Table("stolik0", [3,10], render_order=2, active=True),
    Table("stolik1", [3,9], active=True),
    Table("stolik2", [8,3], active=True),
    Table("stolik3", [7,6], active=False),
    Table("stolik4", [10,12], active=False),
    Table("stolik5", [11,12], active=False)
]

krzesla = [
    Chair("krzeslo0", [3,11], "southwest"),
    Chair("krzeslo1", [3,8], "northeast"),
    Chair("krzeslo2", [4,10], "southeast"),
    Chair("krzeslo3", [8,4], "southwest"),
    Chair("krzeslo4", [9,3], "southeast"),
    Chair("krzeslo5", [7,5], "northeast"),
    Chair("krzeslo6", [10,13], "southwest"),
    Chair("krzeslo7", [11,13], "southwest"),
    Chair("krzeslo8", [12,12], "southeast"),
    Chair("krzeslo9", [10,11], "northeast"),
    Chair("krzeslo10", [11,11], "northeast"),
    Chair("krzeslo11", [9,12], "northwest")
]

stoliki[2].add_chair(krzesla[0])
stoliki[1].add_chair(krzesla[1])
stoliki[1].add_chair(krzesla[2])
stoliki[1].add_chair(krzesla[3])
stoliki[1].add_chair(krzesla[4])

stoliki[1].remove_chair(krzesla[2])
stoliki[2].add_chair(krzesla[2])

klient = Client("klient", [1, 1], [gridSize/2, gridSize/2])
klient.assignTable(stoliki[0])
klient.makeOrder("taco")

klient2 = Client("klient2", [1, 1], [gridSize/2, gridSize/2])
klient2.assignTable(stoliki[1])
klient2.makeOrder("fried_egg")

klient3 = Client("klient3", [1, 1], [gridSize/2, gridSize/2])
klient3.assignTable(stoliki[2])
klient3.makeOrder("pancake")

kelner.recieveOrder(klient)
kelner.recieveOrder(klient2)

kucharz.takeOrderFromWaiter(kelner)
kucharz.makeFood(kelner)

kelner.takeFood(kucharz)
kelner.completeOrder()
