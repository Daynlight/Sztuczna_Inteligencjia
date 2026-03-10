from Classes.Table import Table
from Classes.Chair import Chair
from Classes.Beings.Client import Client
from Classes.Beings.Waiter import Waiter
from Classes.Beings.Cook import Cook
from Classes.Object import Object
from conf import movementSpeed



kelner = Waiter("kelner", [1, 1])
kucharz = Cook("kucharz", [0, 0])

stoliki = [
    Table("stolik0", [8,1], False),
    Table("stolik1", [8,2], True),
    Table("stolik2", [8,3], False),
    Table("stolik3", [8,4], True),
    Table("stolik4", [10,1], False),
    Table("stolik5", [10,2], True),
    Table("stolik6", [10,3], False),
    Table("stolik7", [10,4], True)
]

krzesla = [
    Chair("krzeslo0", [2,4]),
    Chair("krzeslo1", [4,4]),
    Chair("krzeslo2", [3,3]),
    Chair("krzeslo3", [4,2]),
    Chair("krzeslo4", [5,3])
]

stoliki[2].add_chair(krzesla[0])
stoliki[1].add_chair(krzesla[1])
stoliki[1].add_chair(krzesla[2])
stoliki[1].add_chair(krzesla[3])
stoliki[1].add_chair(krzesla[4])

stoliki[1].remove_chair(krzesla[2])
stoliki[2].add_chair(krzesla[2])

klient = Client("klient", [1, 1])
klient.assign_table(stoliki[1])
klient2 = Client("klient2", [1, 1])
klient2.assign_table(stoliki[1])
