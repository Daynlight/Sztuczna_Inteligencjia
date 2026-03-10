from Classes.Object import Object

class Chair(Object):

    def __init__(self, name, position):
        super().__init__(name, 0, "Assets/chair.png", position, 0, [1, 1])

        self.occupied = False
        self.sitter = None
    
    def occupy(self, person):
        if not self.occupied:
            self.occupied = True
            self.sitter = person.name
        else:
            print("Chair is occupited")
    
    def free(self):
        if self.occupied:
            self.occupied = False
            self.sitter = None
        else:
            print("Chair already free")