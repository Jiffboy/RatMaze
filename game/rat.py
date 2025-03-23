import pygame

from vars.direction import Direction
from vars.resources import rat_lookup


class Rat:
    def __init__(self, size):
        self.x = 0
        self.y = 0
        self.size = size
        self.image = pygame.transform.scale(rat_lookup[Direction.RIGHT], (self.size, self.size))

    def do_frame(self):
        pass

    def draw(self, screen):
        x_pos = self.x * self.size
        y_pos = self.y * self.size
        screen.blit(self.image, (x_pos, y_pos))

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_size(self, size):
        self.size = size
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def move_up(self):
        self.y -= 1

    def move_right(self):
        self.x += 1
        self.image = pygame.transform.scale(rat_lookup[Direction.RIGHT], (self.size, self.size))

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1
        self.image = pygame.transform.scale(rat_lookup[Direction.LEFT], (self.size, self.size))
