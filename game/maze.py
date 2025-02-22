import random
import pygame
from mazelib import Maze as Mazelib
from mazelib.generate.HuntAndKill import HuntAndKill

from vars.globals import chat_stats, lock, tile_size, grid_anchor_x, grid_anchor_y
from vars.direction import Direction
from game.tile import Tile
from game.rat import Rat


class Maze:
    def __init__(self, config):
        self.vote_threshold = config.vote_threshold
        self.width = config.grid_width
        self.height = config.grid_height
        self.grid = [[Tile() for x in range(self.width)] for y in range(self.height)]
        self.start = (0, 0)
        self.end = (0, 0)
        self.rat = Rat()
        self.regenerate_maze(random.randrange(0, self.width))

    def regenerate_maze(self, start):
        self.start = (0, start)
        self.end = (0, 0)

        maze = Mazelib()
        # The algorithm generates a maze of size 2 * height + 1 by 2 * width + 1. We need to adjust
        # We want it to be 2 greater than what we need, since it includes an outer wall, and that's stupid
        maze.generator = HuntAndKill(int((self.width - 1) / 2) + 1, int((self.height - 1) / 2) + 1)
        maze.generate()

        # If our start point is a wall, regenerate until it is not
        while maze.grid[1][start + 1]:
            maze.generate()

        self.grid = []
        curr_row = 0
        for row in maze.grid:
            # Do not include first and last rows
            if 0 < curr_row <= self.width:
                tile_row = []
                curr_column = 0
                for column in row:
                    # Do not include first and last column
                    if 0 < curr_column <= self.height:
                        tile = Tile()
                        # true means wall
                        if not column:
                            tile.set_path()
                        tile_row.append(tile)
                    curr_column += 1
                self.grid.append(tile_row)
            curr_row += 1

        viable_exits = []
        y = 0
        end_x = self.width-1
        for i in self.grid[end_x]:
            if i.is_path:
                viable_exits.append(y)
            y += 1

        end_y = random.choice(viable_exits)
        self.end = (end_x, end_y)
        self.grid[self.start[0]][self.start[1]].set_start()
        self.grid[end_x][end_y].set_end()
        self.rat.set_position(self.start[0], self.start[1])

    def resize_maze(self, height, width, start):
        self.width = width
        self.height = height
        self.regenerate_maze(start)

    def do_frame(self):
        with lock:
            if chat_stats.get_vote_count(Direction.UP) >= self.vote_threshold and self.can_move(0, -1):
                self.rat.move_up()
                chat_stats.reset()
            elif chat_stats.get_vote_count(Direction.RIGHT) >= self.vote_threshold and self.can_move(1, 0):
                self.rat.move_right()
                chat_stats.reset()
            elif chat_stats.get_vote_count(Direction.DOWN) >= self.vote_threshold and self.can_move(0, 1):
                self.rat.move_down()
                chat_stats.reset()
            elif chat_stats.get_vote_count(Direction.LEFT) >= self.vote_threshold and self.can_move(-1, 0):
                self.rat.move_left()
                chat_stats.reset()

    def can_move(self, x, y):
        if 0 <= self.rat.y + y < self.height and 0 <= self.rat.x + x < self.width:
            x_check = self.grid[self.rat.x + x][self.rat.y]
            y_check = self.grid[self.rat.x][self.rat.y + y]
            if x_check.is_path and y_check.is_path:
                return True
        return False

    def draw(self, screen):
        full_width = tile_size * (self.width + 2)
        full_height = tile_size * (self.height + 2)
        pygame.draw.rect(screen, (0, 30, 16), (grid_anchor_x - tile_size, grid_anchor_y - tile_size, full_width, full_height))
        grid_x = 0
        for i in self.grid:
            grid_y = 0
            for j in i:
                tile = self.grid[grid_x][grid_y]
                tile_x = grid_anchor_x + (grid_x * tile_size)
                tile_y = grid_anchor_y + (grid_y * tile_size)
                if tile.is_path:
                    pygame.draw.rect(screen, (155, 118, 83), (tile_x, tile_y, tile_size, tile_size))
                if tile.is_end:
                    pygame.draw.rect(screen, (254, 220, 86), (tile_x, tile_y, tile_size, tile_size))
                if tile.is_wall:
                    pygame.draw.rect(screen, (1, 50, 32), (tile_x, tile_y, tile_size, tile_size))
                grid_y += 1
            grid_x += 1
        self.rat.draw(screen)
