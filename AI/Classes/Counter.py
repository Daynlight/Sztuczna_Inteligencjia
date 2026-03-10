from Classes.Object import Object

class Counter(Object):

    def __init__(self, name, position, render_order = 1):
        super().__init__(name, render_order, "Assets/Obstacles/counter02_i.png", position, size=[2,2])
