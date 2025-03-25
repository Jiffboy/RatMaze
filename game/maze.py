import random
import pygame
from mazelib import Maze as Mazelib
from mazelib.generate.HuntAndKill import HuntAndKill

from vars.globals import chat_stats, shop, lock, tile_size, grid_size, grid_anchor_x, grid_anchor_y
from vars.direction import Direction
from game.tile import Tile
from game.rat import Rat


class Maze:
    def __init__(self, config):
        self.vote_threshold = config.vote_threshold
        self.config = config
        self.width = config.init_maze_size
        self.height = config.init_maze_size
        self.grid = []
        self.start = (0, 0)
        self.end = (0, 0)
        self.tile_size = tile_size
        self.rat = Rat(self.tile_size)
        self.surface = pygame.Surface((0, 0))
        self.explosion_length = 250
        self.explosion_timeout = 0
        self.explosion_start = 0
        self.exploded_tiles = []
        self.tiles_to_explode = []
        self.regenerate_maze((1, random.randrange(1, self.width-1)))

    def regenerate_maze(self, rat_pos):
        self.start = rat_pos
        self.end = (0, 0)

        maze = Mazelib()
        # The algorithm generates a maze of size 2 * height + 1 by 2 * width + 1. We need to adjust
        maze.generator = HuntAndKill(int((self.width - 1) / 2), int((self.height - 1) / 2))
        maze.generate()

        # If our start point is a wall, regenerate until it is not
        while maze.grid[rat_pos[0]][rat_pos[1]]:
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
                else:
                    tile.set_wall()
                tile_row.append(tile)
                curr_column += 1
            self.grid.append(tile_row)
            curr_row += 1

        # Second pass to set neighbors and determine an end location
        end_x = self.width - 2
        viable_exits = []
        for x in range(0, self.width):
            for y in range(0, self.height):
                tile = self.grid[x][y]
                if x == end_x and tile.is_path:
                    viable_exits.append(y)
                tile.neighbors[Direction.UP] = self.grid[x][y-1] if y > 0 else None
                tile.neighbors[Direction.LEFT] = self.grid[x-1][y] if x > 0 else None
                tile.neighbors[Direction.DOWN] = self.grid[x][y+1] if y < self.height - 1 else None
                tile.neighbors[Direction.RIGHT] = self.grid[x+1][y] if x < self.width - 1 else None

        # Avoid putting end underneath rat
        end_y = random.choice(viable_exits)
        while end_y == self.rat.get_y() and end_x == self.rat.get_x():
            end_y = random.choice(viable_exits)

        self.end = (end_x, end_y)
        self.grid[self.start[0]][self.start[1]].set_start()
        self.grid[end_x][end_y].set_end()
        self.rat.set_position(self.start[0], self.start[1])
        self.rat.set_size(self.tile_size)
        self.build_surface()

    def resize_maze(self, height, width, rat_pos):
        self.width = width
        self.height = height
        self.regenerate_maze(rat_pos)

    def queue_explosion(self, tiles, explosion_delay=0):
        for tile in tiles:
            if 0 <= tile[0] < self.width:
                if 0 <= tile[1] < self.height:
                    grid_tile = self.grid[tile[0]][tile[1]]
                    if not grid_tile.is_border:
                        self.tiles_to_explode.append(grid_tile)
        self.explosion_start = pygame.time.get_ticks() + explosion_delay

    def destroy_tiles(self):
        for tile in self.tiles_to_explode:
            tile.set_exploded()
            self.exploded_tiles.append(tile)
        self.tiles_to_explode = []
        self.build_surface()
        self.explosion_timeout = pygame.time.get_ticks() + self.explosion_length

    def move(self, direction):
        new_pos = (self.rat.get_x(), self.rat.get_y())
        match direction:
            case Direction.UP:
                new_pos = self.try_move(0, -1)

            case Direction.RIGHT:
                new_pos = self.try_move(1, 0)

            case Direction.DOWN:
                new_pos = self.try_move(0, 1)

            case Direction.LEFT:
                new_pos = self.try_move(-1, 0)

        if new_pos[0] != self.rat.get_x() or new_pos[1] != self.rat.get_y():
            self.rat.move_to(new_pos[0], new_pos[1])
            chat_stats.vote_won(direction)
            return True
        return False

    def do_frame(self):
        with lock:
            if not self.rat.animation_locked:
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
            now = pygame.time.get_ticks()

            if now >= self.explosion_start != 0:
                self.destroy_tiles()
                self.explosion_start = 0

            if now >= self.explosion_timeout and len(self.exploded_tiles) > 0:
                for tile in self.exploded_tiles:
                    tile.unexplode()
                self.exploded_tiles = []
                self.build_surface()
        self.rat.do_frame()

    # I'm not even going to try and explain what happens in this function it is between me and God
    # I will tell myself I am going to clean up this dumpster fire at some point, but I probably won't
    def try_move(self, x, y):
        end_x = self.rat.get_x()
        end_y = self.rat.get_y()
        x_length = x
        y_length = y

        if self.rat.speed_boost:
            x_length = x * 2
            y_length = y * 2

        if x != 0:
            x_range = range(self.rat.get_x(), self.rat.get_x() + x_length + x, x)
            for curr_x in x_range:
                if 0 <= curr_x < self.width:
                    tile = self.grid[curr_x][self.rat.get_y()]
                    if tile.is_path:
                        end_x = curr_x
                        if tile.is_end:
                            break
                    elif self.rat.can_jump:
                        curr_x += x
                        if 0 <= curr_x < self.width:
                            tile = self.grid[curr_x][self.rat.get_y()]
                            if tile.is_path:
                                end_x = curr_x
                                if tile.is_end:
                                    break
                        pass
                    else:
                        break
                else:
                    break

            if end_x != self.rat.get_x():
                return end_x, self.rat.get_y()

        if y != 0:
            for curr_y in range(self.rat.get_y(), self.rat.get_y() + y_length + y, y):
                if 0 <= curr_y < self.height:
                    tile = self.grid[self.rat.get_x()][curr_y]
                    if tile.is_path:
                        end_y = curr_y
                        if tile.is_end:
                            break
                    elif self.rat.can_jump:
                        curr_y += y
                        if 0 <= curr_y < self.height:
                            tile = self.grid[self.rat.get_x()][curr_y]
                            if tile.is_path:
                                end_y = curr_y
                                if tile.is_end:
                                    break
                        pass
                    else:
                        break
                else:
                    break

            if end_y != self.rat.get_y():
                return self.rat.get_x(), end_y

        return self.rat.get_x(), self.rat.get_y()

    def build_surface(self):
        full_width = self.tile_size * self.width
        full_height = self.tile_size * self.height
        self.surface = pygame.Surface((full_width, full_height))
        for row in self.grid:
            for tile in row:
                tile.build_image()
                tile.draw(self.surface)

    def draw(self, screen):

        surface = self.surface.copy()
        self.rat.draw(surface)
        surface = pygame.transform.scale(surface, (grid_size, grid_size))
        screen.blit(surface, (grid_anchor_x, grid_anchor_y))

    def has_won(self):
        return self.grid[self.rat.get_x()][self.rat.get_y()].is_end

    def complete_reset(self):
        chat_stats.full_reset()
        shop.cleanup_items(self)
        shop.reset()
        start = (1, random.randrange(1, self.config.init_maze_size-2))
        self.resize_maze(self.config.init_maze_size, self.config.init_maze_size, start)

    def eat_cheese(self):
        self.grid[self.end[0]][self.end[1]].eat_cheese()
        self.rat.eat_cheese()
        self.build_surface()
