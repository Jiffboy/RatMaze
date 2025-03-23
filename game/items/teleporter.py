import random

from game.items.item import Item


class Teleporter(Item):
    def use(self, maze):
        x = maze.rat.x
        y = maze.rat.y

        tile_list = []

        for curr_x in range(1, maze.width):
            for curr_y in range(1, maze.height):
                if maze.grid[curr_x][curr_y].is_path and not maze.grid[curr_x][curr_y].is_end:
                    if curr_x != maze.rat.x and curr_y != maze.rat.y:
                        tile_list.append((curr_x, curr_y))

        new_spot = random.choice(tile_list)
        maze.rat.x = new_spot[0]
        maze.rat.y = new_spot[1]
        super().use(maze)
