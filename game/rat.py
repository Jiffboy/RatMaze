import pygame

from vars.globals import tile_size, grid_anchor_y, grid_anchor_x


class Rat:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = pygame.transform.scale(pygame.image.load("resources/images/rat/right.png"), (tile_size, tile_size))

    def do_frame(self):
        pass

    def draw(self, screen):
        x_pos = grid_anchor_x + (self.x * tile_size)
        y_pos = grid_anchor_y + (self.y * tile_size)
        screen.blit(self.image, (x_pos, y_pos))

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def move_up(self):
        self.y -= 1
        self.image = pygame.transform.scale(pygame.image.load("resources/images/rat/up.png"), (tile_size, tile_size))

    def move_right(self):
        self.x += 1
        self.image = pygame.transform.scale(pygame.image.load("resources/images/rat/right.png"), (tile_size, tile_size))

    def move_down(self):
        self.y += 1
        self.image = pygame.transform.scale(pygame.image.load("resources/images/rat/down.png"), (tile_size, tile_size))

    def move_left(self):
        self.x -= 1
        self.image = pygame.transform.scale(pygame.image.load("resources/images/rat/left.png"), (tile_size, tile_size))
