import pygame

from vars.globals import tile_size


def build_lookup(image_path, frames, row):
    lookup = []
    image = pygame.image.load(image_path)
    for x in range(frames):
        rect = pygame.Rect(x * tile_size, row * tile_size, tile_size, tile_size)
        frame = image.subsurface(rect)
        lookup.append(frame)
    return lookup


# Tiles
path_img = pygame.image.load("resources/images/tiles/path.png")
cheese_img = pygame.image.load("resources/images/tiles/cheese.png")
explosion_img = pygame.image.load("resources/images/tiles/explosion.png")

walls_lookup = build_lookup("resources/images/tiles/walls.png", 16, 0)
borders_lookup = build_lookup("resources/images/tiles/borders.png", 8, 0)
rat_idle_right_lookup = build_lookup("resources/images/rat/rat.png", 5, 0)
rat_idle_left_lookup = build_lookup("resources/images/rat/rat.png", 5, 1)
rat_walking_right_lookup = build_lookup("resources/images/rat/rat.png", 3, 2)
rat_walking_left_lookup = build_lookup("resources/images/rat/rat.png", 3, 3)
rat_cheese_right_lookup = build_lookup("resources/images/rat/rat.png", 8, 4)
rat_cheese_left_lookup = build_lookup("resources/images/rat/rat.png", 8, 5)
rat_jump_right_lookup = build_lookup("resources/images/rat/rat.png", 2, 6)
rat_jump_left_lookup = build_lookup("resources/images/rat/rat.png", 2, 7)

rat_idle_fps = 7
rat_walking_fps = 9
rat_cheese_fps = 6
rat_jump_fps = 9
