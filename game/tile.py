import pygame
from vars.globals import grid_anchor_x, grid_anchor_y


class Tile:
    def __init__(self, x, y, tile_size):
        self.is_path = False
        self.is_wall = True
        self.is_start = False
        self.is_end = False
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.image = pygame.transform.scale(pygame.image.load("resources/images/tiles/wall.png"), (tile_size, tile_size))

    def set_wall(self):
        self.is_path = False
        self.is_wall = True
        self.image = pygame.transform.scale(pygame.image.load("resources/images/tiles/wall.png"), (self.tile_size, self.tile_size))

    def set_path(self):
        self.is_wall = False
        self.is_path = True
        self.image = pygame.transform.scale(pygame.image.load("resources/images/tiles/path.png"), (self.tile_size, self.tile_size))

    def set_start(self):
        self.is_path = True
        self.is_start = True
        self.image = pygame.transform.scale(pygame.image.load("resources/images/tiles/path.png"), (self.tile_size, self.tile_size))

    def set_end(self):
        self.is_path = True
        self.is_end = True
        self.image = pygame.transform.scale(pygame.image.load("resources/images/tiles/cheese.png"), (self.tile_size, self.tile_size))

    def draw(self, screen):
        x_pos = grid_anchor_x + (self.x * self.tile_size)
        y_pos = grid_anchor_y + (self.y * self.tile_size)
        screen.blit(self.image, (x_pos, y_pos))
