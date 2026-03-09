import numpy as np
import pygame
from Classes.World import Camera

class Grid:
    def __init__(self, size_x: int, size_y: int, tile_size : int, margin_top : int, margin_left: int):
        self.size_x = size_x
        self.size_y = size_y
        self.tile_size = tile_size
        self.margin_top = margin_top
        self.margin_left = margin_left

        self.tiles = []

        for y in range(0, self.size_y):
            row = []

            for x in range(0, self.size_x):
                tile = Tile(margin_left + ((size_x + y - x)  * tile_size), margin_top + (tile_size / 2 + (y + x)* tile_size/2), tile_size, y, x) # Loop for correct tiles placement
                row.append(tile)

            self.tiles.append(row)

    def __del__(self):
        for row in self.tiles:
            for tile in row:
                del tile
        self.tiles.clear()

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
    #The most important part of object of class Tile is center_x and center_y, based on them is calulated rhombus (diament) with dimensions a x 2a 
    def __init__(self, center_x, center_y, a, isometric_x, isometric_y):
        self.center_x = center_x
        self.center_y = center_y
        self.a = a
        self.top_corner = np.array([center_x, center_y - a/2])      #top_corner of rhombus
        self.right_corner = np.array([center_x + a, center_y])      #top_corner of rhombus
        self.bottom_corner = np.array([center_x, center_y + a/2])
        self.left_corner = np.array([center_x - a, center_y])
        self.isometric_x = isometric_x
        self.isometric_y = isometric_y

    def __del__(self):
        self.top_corner = None
        self.right_corner = None
        self.down_corner = None
        self.left_corner = None


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
        pygame.draw.polygon(target_surface, (0, 255, 0), (self.top_corner, self.right_corner, self.bottom_corner, self.left_corner))
        pygame.draw.line(target_surface, (0, 0, 0), self.left_corner, self.top_corner)
        pygame.draw.line(target_surface, (0, 0, 0), self.top_corner, self.right_corner)
        pygame.draw.line(target_surface, (0, 0, 0), self.right_corner, self.bottom_corner)
        pygame.draw.line(target_surface, (0, 0, 0), self.bottom_corner, self.left_corner)

