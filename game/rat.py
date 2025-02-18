import pygame

from vars.globals import tile_size, grid_anchor_y, grid_anchor_x


class Rat:
    def __init__(self):
        self.x = 0
        self.y = 0

    def do_frame(self):
        pass

    def draw(self, screen):
        x_pos = grid_anchor_x + (self.x * tile_size)
        y_pos = grid_anchor_y + (self.y * tile_size)
        pygame.draw.rect(screen, (150, 150, 150), (x_pos, y_pos, tile_size, tile_size))

        # nose :)
        nose_size = tile_size / 4
        nose_gap_y = tile_size / 2 - (nose_size / 2)
        nose_gap_x = tile_size - nose_size
        pygame.draw.rect(screen, (251, 198, 207), (x_pos + nose_gap_x, y_pos + nose_gap_y, nose_size, nose_size))

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def move_up(self):
        self.y -= 1

    def move_right(self):
        self.x += 1

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1
