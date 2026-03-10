from Classes.Object import Object

class Being(Object):
    def __init__(self, name, render_order, texture_path, position, velocity, size):
        super().__init__(name, render_order, texture_path, position, velocity, size)