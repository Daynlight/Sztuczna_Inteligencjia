import os
import numpy as np
from enum import Enum

from Classes.Core.Object.Object import Object
from Classes.Core.Renderer.Texture import Texture

from Classes.Objects.Beings.Client import Client
import Classes.Objects.TextureManager as TextureManager


class ChairInterface(Object):
    def __init__(self, position: np.ndarray[int], texture: Texture, render_order: int = 0, size: np.ndarray[int] = np.array([1,1]), offset: np.ndarray[int] = np.array([0, 0])):
        super().__init__(render_order = render_order, texture = texture ,position = position, size = size, offset= offset)

        self._occupied: bool = False
        self._client: Client | None = None
        self._table = None

    def getClient(self) -> Client:
        return self._client
    
    def getTable(self):
        return self._table
    
    def setTable(self, table) -> None:
        self._table = table

    def sitClient(self, client: Client) -> None:
        if not self.getClient():
            self._occupied: bool = True
            self._client: list[Client] = client

    def free(self) -> None:
        if self._occupied:
            self._occupied: bool = False
            self._client: list[Client] = None

    
