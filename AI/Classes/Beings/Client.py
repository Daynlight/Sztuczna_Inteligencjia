from Classes.Being import Being

class Client(Being):

    def __init__(self, name, position):
        super().__init__(name, 2, "Assets/Other/client.png", position, velocity=2)

        self.table = None
        self.chair = None
        self.waiting = False
        self.eating = False
        self.what_food = None
    
    def assignTable(self,table):
        for chair in table.chairs:
            if not chair.occupied:
                self.table=table
                self.chair=chair
                chair.occupy(self)
                self.setPosition(chair.position)
                return
        print("Table "+table.name+" is full")

    def makeOrder(self, food_name):
        self.waiting = True
        self.what_food = food_name
    
    def recieveFood(self):
        self.waiting = False
        self.eating = True