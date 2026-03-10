from Classes.Object import Object

class Table(Object):

    def __init__(self, name, position, active=False):
        super().__init__(name, 0, "Assets/obstacle.png", position, [1, 1])

        self.active = active
        self.chairs = []

    def seatClient(self, client):
        self.client = client
        self.occupied = True

    def freeTable(self):
        self.client = None
        self.occupied = False

    def addChair(self,chair):
        self.chairs.append(chair)
    
    def removeChair(self,chair):
        if chair in self.chairs:
            self.chairs.remove(chair)
        else:
            print("That chair isn't next to this table")