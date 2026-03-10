from Classes.Object import Object

class Table(Object):

    def __init__(self, name, position, active=False):
        super().__init__(name, 0, "Assets/obstacle.png", position, 0, [1, 1])

        self.active = active
        self.chairs = []

    def seat_client(self, client):
        self.client = client
        self.occupied = True

    def free_table(self):
        self.client = None
        self.occupied = False

    def add_chair(self,chair):
        self.chairs.append(chair)
    
    def remove_chair(self,chair):
        if chair in self.chairs:
            self.chairs.remove(chair)
        else:
            print("That chair isn't next to this table")