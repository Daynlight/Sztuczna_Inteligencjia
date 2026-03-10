from Classes.Being import Being

class Cook(Being):

    def __init__(self, name, position):
        super().__init__(name, 2, "Assets/kucharz.png", position, 0, [1,1])

        self.current_order = None