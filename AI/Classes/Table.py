from Classes.Object import Object

class Table(Object):

    def __init__(self, name, position, active=False):
        super().__init__(name, 0, "Assets/obstacle.png", position, 0, [1, 1])

        self.active = active
        self.occupied = False
        self.client = None

    def seat_client(self, client):
        self.client = client
        self.occupied = True

    def free_table(self):
        self.client = None
        self.occupied = False