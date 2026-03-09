from Classes.Table import Table
from Classes.Object import Object
from conf import movementSpeed



kelner = Object("kelner", 3, "Assets/jenkins.png", [1, 1], movementSpeed, [1, 1])
kucharz = Object("kucharz", 2, "Assets/kucharz.png", [0, 0], 0, [1, 1])

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
klient = Object("klient", 1, "Assets/client.png", stoliki[1].position, 0, [1, 1])
