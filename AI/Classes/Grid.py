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
        self.nodes = []
        
        for y in range(self.size_y + 1):
            row = []

            for x in range(self.size_x + 1):
                x_pos = margin_left + (size_x + x - y) * (tile_size)
                y_pos = margin_top + (x + y) * (tile_size / 2) 
                node = Node(x_pos, y_pos)
                row.append(node)
            self.nodes.append(row)


        for y in range(0, self.size_y):
            row = []

            for x in range(0, self.size_x):
                tile = Tile(
                    margin_left + ((size_x + y - x)  * tile_size), 
                    margin_top + (tile_size / 2 + (y + x)* tile_size/2), 
                    tile_size, 
                    y, 
                    x
                )
                tile.top_corner = self.nodes[x][y]
                tile.right_corner = self.nodes[x][y + 1]
                tile.bottom_corner = self.nodes[x + 1][y +1 ]
                tile.left_corner = self.nodes[x + 1][y] 
                row.append(tile)

            self.tiles.append(row)
            
        self.walles = [Wall(self.nodes[0][0], self.nodes[size_y][0], 100),
        Wall(self.nodes[0][0], self.nodes[0][size_x], 100),]

        

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

        for y in range(len(self.nodes)):
            for x in range(len(self.nodes[y])):
                node = self.nodes[y][x]

                if x + 1 < len(self.nodes[y]):
                    right_node = self.nodes[y][x + 1]
                    pygame.draw.line(surface, (156, 128, 112), node.get(), right_node.get())
                if y + 1 < len(self.nodes):
                    bottom_node = self.nodes[y + 1][x]
                    pygame.draw.line(surface, (156, 128, 112), node.get(), bottom_node.get())
        for wall in self.walles:
            wall.draw(surface)
        

class Tile:
    #The most important part of object of class Tile is center_x and center_y, based on them is calulated rhombus (diament) with dimensions a x 2a 
    def __init__(self, center_x, center_y, a, isometric_x, isometric_y):
        self.center_x = center_x
        self.center_y = center_y
        self.a = a
        self.top_corner = None
        self.right_corner = None
        self.bottom_corner = None
        self.left_corner = None
        self.isometric_x = isometric_x
        self.isometric_y = isometric_y

    def __del__(self):
        self.top_corner = None
        self.right_corner = None
        self.bottom_corner = None
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
        pygame.draw.polygon(target_surface, (204, 169, 149), (self.top_corner.get(), self.right_corner.get(), self.bottom_corner.get(), self.left_corner.get()))

class Node:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
    def get(self):
        return(self.pos_x, self.pos_y)
    
class Wall:
    def __init__(self, node_1 : Node, node_2 : Node, height : int):
        self.node_1 = node_1
        self.node_2 = node_2
        self.height = height
    def draw(self, surface):
        x_1, y_1 = self.node_1.get()
        x_2, y_2 = self.node_2.get()

        points = (
            (x_1, y_1),
            (x_2, y_2),
            (x_2, y_2 - self.height),
            (x_1, y_1 - self.height)
        )

        pygame.draw.polygon(surface, (245, 160, 95), points)

        pygame.draw.polygon(surface, (0, 0, 0), points, 1) 
