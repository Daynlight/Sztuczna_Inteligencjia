import pygame

class World:
    def __init__(self, width : int, height : int):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height))
    def draw(self):
        self.surface.fill((41, 40, 40))


class Camera:
    def __init__(self, width: int, height: int, center_x_pos, center_y_pos):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.center_x_pos = center_x_pos
        self.center_y_pos = center_y_pos

    def update(self):
        self.camera.x = self.center_x_pos - self.width // 2
        self.camera.y = self.center_y_pos - self.height // 2