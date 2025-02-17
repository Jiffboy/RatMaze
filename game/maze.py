import random
import pygame

from vars.globals import tile_size
from game.tile import Tile


class Maze:
    def __init__(self, config, x, y):
        self.x = x
        self.y = y
        self.width = config.grid_width
        self.height = config.grid_height
        self.grid = [[Tile() for x in range(self.width)] for y in range(self.height)]
        self.start = (0, 0)
        self.end = (0, 0)
        self.regenerate_maze(random.randrange(0, self.width))

    # Chaos reigns in this domain, there will be no comments here.
    def take_step(self, x, y):
        self.grid[x][y].set_path()
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        random.shuffle(directions)

        while len(directions) > 0:
            dir = directions.pop()
            curr_x = x + (dir[0] * 2)
            curr_y = y + (dir[1] * 2)

            if 0 <= curr_x < self.width and 0 <= curr_y < self.height:
                if self.grid[curr_x][curr_y].is_wall:
                    skipped_x = x + dir[0]
                    skipped_y = y + dir[1]
                    self.grid[skipped_x][skipped_y].set_path()

                    self.take_step(curr_x, curr_y)

    def regenerate_maze(self, start):
        self.grid = [[Tile() for x in range(self.width)] for y in range(self.height)]
        self.grid[0][start].set_start()
        self.start = (0, start)
        self.end = (0, 0)
        self.take_step(0, start)

        viable_exits = []
        y = 0
        end_x = self.width-1
        for i in self.grid[end_x]:
            if i.is_path:
                viable_exits.append(y)
            y += 1

        end_y = random.choice(viable_exits)
        self.end = (end_x, end_y)
        self.grid[end_x][end_y].set_end()

    def resize_maze(self, height, width, start):
        self.width = width
        self.height = height
        self.regenerate_maze(start)

    def draw(self, screen):
        grid_x = 0
        for i in self.grid:
            grid_y = 0
            for j in i:
                tile = self.grid[grid_x][grid_y]
                tile_x = self.x + (grid_x * tile_size)
                tile_y = self.y + (grid_y * tile_size)
                if tile.is_start:
                    pygame.draw.rect(screen, (0, 128, 0), (tile_x, tile_y, tile_size, tile_size))
                if tile.is_end:
                    pygame.draw.rect(screen, (128, 0, 0), (tile_x, tile_y, tile_size, tile_size))
                if tile.is_wall:
                    pygame.draw.rect(screen, (0, 0, 0), (tile_x, tile_y, tile_size, tile_size))
                grid_y += 1
            grid_x += 1
