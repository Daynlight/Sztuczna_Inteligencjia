import numpy as np
import pygame
from Classes.World import Camera

class Grid:
    def __init__(self, size_x, size_y, tile_size, margin_top, margin_left):
        self.size_x = size_x
        self.size_y = size_y
        self.tile_size = tile_size
        self.margin_top = margin_top
        self.margin_left = margin_left

        self.tiles = []

        for y in range(0, self.size_y):
            row = []

            for x in range(0, self.size_x):
                tile = Tile(margin_left + ((size_x + y - x)  * tile_size), margin_top + (tile_size / 2 + (y + x)* tile_size/2), tile_size, y, x) #+100 offest from window
                row.append(tile)

            self.tiles.append(row)

    def get_hovered_tile(self, mouse_pos, camera : Camera):
        for row in self.tiles:
            for tile in row:
                if tile.isHovered(mouse_pos, camera):
                    return tile
        return None

    def draw(self, surface):
        for row in self.tiles:
            for tile in row:
                tile.draw(surface)
        

class Tile:
    def __init__(self, center_x, center_y, a, isometric_x, isometric_y):
        self.center_x = center_x
        self.center_y = center_y
        self.a = a
        self.top_corner = np.array([center_x, center_y - a/2])
        self.right_corner = np.array([center_x + a, center_y])
        self.down_corner = np.array([center_x, center_y + a/2])
        self.left_corner = np.array([center_x - a, center_y])
        self.surface = pygame.Surface((2*a, a))
        self.isometric_x = isometric_x
        self.isometric_y = isometric_y


    def isHovered(self, mouse_pos, camera : Camera):
        x, y = mouse_pos

        world_x = x + camera.camera.x
        world_y = y + camera.camera.y

        dx = abs(world_x - self.center_x)
        dy = abs(world_y - self.center_y)

        if dx / self.a + dy / (self.a / 2) <= 1:
            return True
        return False

    def draw(self, target_surface):
        pygame.draw.polygon(target_surface, (0, 255, 0), (self.top_corner, self.right_corner, self.down_corner, self.left_corner))
        pygame.draw.line(target_surface, (0, 0, 0), self.left_corner, self.top_corner)
        pygame.draw.line(target_surface, (0, 0, 0), self.top_corner, self.right_corner)
        pygame.draw.line(target_surface, (0, 0, 0), self.right_corner, self.down_corner)
        pygame.draw.line(target_surface, (0, 0, 0), self.down_corner, self.left_corner)

