import pygame

from vars.direction import Direction
from vars.resources import walls_lookup, path_img, cheese_img, borders_lookup, explosion_img


class Tile:
    def __init__(self, x, y, tile_size):
        self.is_path = False
        self.is_wall = True
        self.is_start = False
        self.is_end = False
        self.is_border = False
        self.is_exploded = False
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.neighbors = {
            Direction.UP: None,
            Direction.LEFT: None,
            Direction.DOWN: None,
            Direction.RIGHT: None
        }
        self.image = pygame.transform.scale(path_img, (self.tile_size, self.tile_size))

    def set_wall(self):
        self.is_path = False
        self.is_wall = True

    def set_path(self):
        self.is_wall = False
        self.is_path = True

    def set_start(self):
        self.is_path = True
        self.is_start = True

    def set_end(self):
        self.is_path = True
        self.is_end = True

    def set_border(self):
        self.is_path = False
        self.is_wall = True
        self.is_border = True

    def set_exploded(self):
        if not self.is_exploded:
            self.is_exploded = True

    def unexplode(self):
        self.is_exploded = False
        self.set_path()

    def get_wall_number(self):
        up = self.neighbors[Direction.UP]
        left = self.neighbors[Direction.LEFT]
        down = self.neighbors[Direction.DOWN]
        right = self.neighbors[Direction.RIGHT]

        is_up = False if up is None else up.is_wall and not up.is_border
        is_left = False if left is None else left.is_wall and not left.is_border
        is_down = False if down is None else down.is_wall and not down.is_border
        is_right = False if right is None else right.is_wall and not right.is_border

        return int(is_up) << 3 | int(is_left) << 2 | int(is_down) << 1 | int(is_right)

    def get_border_number(self):
        # We only care about cases where there's two bits, so make a lookup map
        lookup = {5: 0, 10: 1, 12: 2, 19: 3, 21: 4, 22: 5, 25: 6, 26: 7}

        up = self.neighbors[Direction.UP]
        left = self.neighbors[Direction.LEFT]
        down = self.neighbors[Direction.DOWN]
        right = self.neighbors[Direction.RIGHT]

        is_zero = self.x == 0 or self.y == 0
        is_up = False if up is None else up.is_border
        is_left = False if left is None else left.is_border
        is_down = False if down is None else down.is_border
        is_right = False if right is None else right.is_border

        return lookup[int(is_zero) << 4 | int(is_up) << 3 | int(is_left) << 2 | int(is_down) << 1 | int(is_right)]

    def build_image(self):
        # Everything is on top of the path
        self.image = pygame.transform.scale(path_img, (self.tile_size, self.tile_size))

        if self.is_end:
            cheese = pygame.transform.scale(cheese_img, (self.tile_size, self.tile_size))
            self.image.blit(cheese, (0, 0))

        elif self.is_border:
            number = self.get_border_number()
            border_img = borders_lookup[number]
            border = pygame.transform.scale(border_img, (self.tile_size, self.tile_size))
            self.image.blit(border, (0, 0))

        elif self.is_wall:
            number = self.get_wall_number()
            wall_img = walls_lookup[number]
            wall = pygame.transform.scale(wall_img, (self.tile_size, self.tile_size))
            self.image.blit(wall, (0, 0))

        if self.is_exploded:
            explosion = pygame.transform.scale(explosion_img, (self.tile_size, self.tile_size))
            self.image.blit(explosion, (0, 0))

    def draw(self, screen):
        x_pos = self.x * self.tile_size
        y_pos = self.y * self.tile_size
        screen.blit(self.image, (x_pos, y_pos))
