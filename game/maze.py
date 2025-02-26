import random
import pygame
from mazelib import Maze as Mazelib
from mazelib.generate.HuntAndKill import HuntAndKill

from vars.globals import chat_stats, lock, tile_size, grid_size, grid_anchor_x, grid_anchor_y
from vars.direction import Direction
from game.tile import Tile
from game.rat import Rat


class Maze:
    def __init__(self, config):
        self.vote_threshold = config.vote_threshold
        self.width = config.init_width
        self.height = config.init_height
        self.grid = []
        self.start = (0, 0)
        self.end = (0, 0)
        self.tile_size = tile_size
        self.rat = Rat(self.tile_size)
        self.surface = pygame.Surface((0, 0))
        self.regenerate_maze(random.randrange(0, self.width))

    def regenerate_maze(self, start):
        self.start = (1, start)
        self.end = (0, 0)

        maze = Mazelib()
        # The algorithm generates a maze of size 2 * height + 1 by 2 * width + 1. We need to adjust
        maze.generator = HuntAndKill(int((self.width - 1) / 2), int((self.height - 1) / 2))
        maze.generate()

        # If our start point is a wall, regenerate until it is not
        while maze.grid[1][start]:
            maze.generate()

        self.grid = []
        curr_row = 0
        for row in maze.grid:
            tile_row = []
            curr_column = 0
            for column in row:
                tile = Tile(curr_row, curr_column, self.tile_size)
                # true means wall
                if not column:
                    tile.set_path()
                # mark the outer walls
                elif not (0 < curr_row < self.width - 1) or not (0 < curr_column < self.height - 1):
                    tile.set_border()
                tile_row.append(tile)
                curr_column += 1
            self.grid.append(tile_row)
            curr_row += 1

        viable_exits = []
        y = 0
        end_x = self.width-2
        for i in self.grid[end_x]:
            if i.is_path:
                viable_exits.append(y)
            y += 1

        end_y = random.choice(viable_exits)
        self.end = (end_x, end_y)
        self.grid[self.start[0]][self.start[1]].set_start()
        self.grid[end_x][end_y].set_end()
        self.rat.set_position(self.start[0], self.start[1])
        self.rat.set_size(self.tile_size)
        self.build_surface()

    def resize_maze(self, height, width, start):
        self.width = width
        self.height = height
        self.regenerate_maze(start)

    def move(self, direction):
        match direction:
            case Direction.UP:
                if self.can_move(0, -1):
                    self.rat.move_up()
                    chat_stats.vote_won(Direction.UP)
                    return True

            case Direction.RIGHT:
                if self.can_move(1, 0):
                    self.rat.move_right()
                    chat_stats.vote_won(Direction.RIGHT)
                    return True

            case Direction.DOWN:
                if self.can_move(0, 1):
                    self.rat.move_down()
                    chat_stats.vote_won(Direction.DOWN)
                    return True

            case Direction.LEFT:
                if self.can_move(-1, 0):
                    self.rat.move_left()
                    chat_stats.vote_won(Direction.LEFT)
                    return True
        return False

    def do_frame(self):
        with lock:
            if chat_stats.is_time_up():
                directions = chat_stats.get_random_directions()
                for direction in directions:
                    if self.move(direction):
                        return
                chat_stats.reset_timeout()
                chat_stats.reset_votes()

            if chat_stats.get_vote_count(Direction.UP) >= self.vote_threshold:
                self.move(Direction.UP)
            elif chat_stats.get_vote_count(Direction.RIGHT) >= self.vote_threshold:
                self.move(Direction.RIGHT)
            elif chat_stats.get_vote_count(Direction.DOWN) >= self.vote_threshold:
                self.move(Direction.DOWN)
            elif chat_stats.get_vote_count(Direction.LEFT) >= self.vote_threshold:
                self.move(Direction.LEFT)

    def can_move(self, x, y):
        if 0 <= self.rat.y + y < self.height and 0 <= self.rat.x + x < self.width:
            x_check = self.grid[self.rat.x + x][self.rat.y]
            y_check = self.grid[self.rat.x][self.rat.y + y]
            if x_check.is_path and y_check.is_path:
                return True
        return False

    def build_surface(self):
        full_width = self.tile_size * self.width
        full_height = self.tile_size * self.height
        self.surface = pygame.Surface((full_width, full_height))
        for row in self.grid:
            for tile in row:
                tile.draw(self.surface)

    def draw(self, screen):

        surface = self.surface.copy()
        self.rat.draw(surface)
        surface = pygame.transform.scale(surface, (grid_size, grid_size))
        screen.blit(surface, (grid_anchor_x, grid_anchor_y))

    def has_won(self):
        return self.grid[self.rat.x][self.rat.y].is_end
