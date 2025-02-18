import random
import pygame

from vars.globals import chat_stats, lock, tile_size, grid_anchor_x, grid_anchor_y
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
        self.rat.set_position(self.start[0], self.start[1])

    def resize_maze(self, height, width, start):
        self.width = width
        self.height = height
        self.regenerate_maze(start)

    def do_frame(self):
        with lock:
            if chat_stats.up >= self.vote_threshold and self.can_move(0, -1):
                self.rat.move_up()
                chat_stats.reset()
            elif chat_stats.right >= self.vote_threshold and self.can_move(1, 0):
                self.rat.move_right()
                chat_stats.reset()
            elif chat_stats.down >= self.vote_threshold and self.can_move(0, 1):
                self.rat.move_down()
                chat_stats.reset()
            elif chat_stats.left >= self.vote_threshold and self.can_move(-1, 0):
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
