from Classes.Being import Being

class Client(Being):

    def __init__(self, name, position):
        super().__init__(name,1,"Assets/client.png",position,2,[1,1])

        self.table = None
        self.chair = None
    
    def assign_table(self,table):
        for chair in table.chairs:
            if not chair.occupied:
                self.table=table
                self.chair=chair
                chair.occupy(self)
                self.setPosition(chair.position)
                return
        print("Table "+table.name+" is full")
