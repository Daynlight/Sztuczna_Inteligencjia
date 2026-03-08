from Classes.Object import Object
from conf import movementSpeed


kelner = Object("kelner", "Assets/jenkins.png", [1, 1], movementSpeed, [1, 1])
kucharz = Object("kucharz", "Assets/kucharz.png", [0, 0], 0, [1, 1])
stolik = Object("stolik", "Assets/obstacle.png", [2, 2], 0, [1, 1])
stolik1 = Object("stolik1", "Assets/obstacle.png", [4, 3], 0, [1, 1])
stolik2 = Object("stolik2", "Assets/obstacle.png", [2, 3], 0, [1, 1])
stolik2 = Object("stolik3", "Assets/obstacle.png", [7, 5], 0, [1, 1])
klient = Object("klient", "Assets/client.png", stolik1.position, 0, [1, 1])