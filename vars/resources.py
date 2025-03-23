import pygame

from vars.direction import Direction
from vars.globals import tile_size

# Tiles
path_img = pygame.image.load("resources/images/tiles/path.png")
cheese_img = pygame.image.load("resources/images/tiles/cheese.png")
explosion_img = pygame.image.load("resources/images/tiles/explosion.png")

walls_img = pygame.image.load("resources/images/tiles/walls.png")
walls_lookup = []

border_img = pygame.image.load("resources/images/tiles/borders.png")
borders_lookup = []

rat_left_img = pygame.image.load("resources/images/rat/left.png")
rat_right_img = pygame.image.load("resources/images/rat/right.png")
rat_lookup = { Direction.LEFT: rat_left_img, Direction.RIGHT: rat_right_img }

for x in range(16):
    rect = pygame.Rect(x * tile_size, 0, tile_size, tile_size)
    wall = walls_img.subsurface(rect)
    walls_lookup.append(wall)

for x in range(8):
    rect = pygame.Rect(x * tile_size, 0, tile_size, tile_size)
    wall = border_img.subsurface(rect)
    borders_lookup.append(wall)