import numpy as np
import pygame

class Grid:
    def __init__(self, size_x, size_y, tile_size):
        self.size_x = size_x
        self.size_y = size_y
        self.tile_size = tile_size

        self.tiles = []

        for y in range(0, self.size_y):
            row = []

            for x in range(0, self.size_x):
                tile = Tile((size_x + y - x)  * tile_size, tile_size / 2 + (y + x)* tile_size/2, tile_size) #+100 offest from window
                row.append(tile)

            self.tiles.append(row)

    def draw(self, surface):
        for row in self.tiles:
            for tile in row:
                tile.draw(surface)
        

class Tile:
    def __init__(self, center_x, center_y, a):
        self.center_x = center_x
        self.center_y = center_y
        self.a = a
        self.top_corner = np.array([center_x, center_y - a/2])
        self.right_corner = np.array([center_x + a, center_y])
        self.down_corner = np.array([center_x, center_y + a/2])
        self.left_corner = np.array([center_x - a, center_y])
        self.surface = pygame.Surface((2*a, a))
        self.surface.fill((255, 0, 0)) # red for debug purposes

    def draw(self, target_surface):
        pygame.draw.polygon(target_surface, (0, 255, 0), (self.top_corner, self.right_corner, self.down_corner, self.left_corner))
        pygame.draw.line(target_surface, (0, 0, 0), self.left_corner, self.top_corner)
        pygame.draw.line(target_surface, (0, 0, 0), self.top_corner, self.right_corner)
        pygame.draw.line(target_surface, (0, 0, 0), self.right_corner, self.down_corner)
        pygame.draw.line(target_surface, (0, 0, 0), self.down_corner, self.left_corner)

