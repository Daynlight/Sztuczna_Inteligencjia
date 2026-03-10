from Classes.Object import Object

class Food(Object):

    def __init__(self, name, position):
        super().__init__(name, 3, f"Assets/Food/{name}_dish.png", position)

