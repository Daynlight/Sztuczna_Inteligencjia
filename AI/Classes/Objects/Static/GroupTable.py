from Classes.Objects.Static.Table import Table

class GroupTable(Table):

    def __init__(self, name, table):
        super().__init__(table._position, table._render_order)
        
        self.tables=[table]
        
    def addTable(self, table):
        if table.getGroup() == None:
            self.tables.append(table)
            table.setGroup(self)
        else:
            print("Table is alredy in another group remove it first")
        
    def removeTable(self, table):
        if table in self.tables:
            self.tables.pop(table)
            table.setGroup(None)
            if len(self.tables) == 0:
                self.__del__()
        else:
            print("That table isn't here")