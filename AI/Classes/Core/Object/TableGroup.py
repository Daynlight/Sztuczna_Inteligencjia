import numpy as np

from Classes.Core.Object.Object import Object
from Classes.Core.Object.ChairInterface import ChairInterface
from Classes.Objects.Static.Chair import Chair
from Classes.Objects.Static.Couch import Couch
from Classes.Objects.Static.Table import Table
from Classes.Objects.Beings.Client import Client

class TableGroup:
    def __init__(self, tables: list[Table] = None, chairinterfaces: list[ChairInterface] = None):

        self._clients: list[Client] = list([])
        self._chairinterface: list[ChairInterface] = chairinterfaces if chairinterfaces else list([])
        self._tables: list[Table] = tables if tables else list([])
        self._occupied: bool = False

    #I miss C++ where I could just create multiple constructors, C++ my beloved

    def seatClients(self, clients: np.ndarray[Client]) -> None:
        self._clients: np.ndarray[Client] = clients
        self._occupied = True

    def free(self) -> None:
        self._clients: list[Client] = list([], dtype=Client)
        self._occupied = False

    def getChairInterface(self) -> list[ChairInterface]:
        return self._chairinterface
    
    def getTables(self) -> list[Table]:
        return self._tables
    
    def getClients(self) -> list[Client]:
        return self._clients

