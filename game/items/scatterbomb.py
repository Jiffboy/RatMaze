import random

from game.items.item import Item


class ScatterBomb(Item):
    def __init__(self, name, used_by, ratio):
        self.ratio = ratio
        super().__init__(name, used_by, sound="resources/audio/skibidi-bop.mp3")

    def use(self, maze):
        tile_list = []

        for curr_x in range(1, maze.width):
            for curr_y in range(1, maze.height):
                tile_list.append((curr_x, curr_y))

        maze.queue_explosion(random.sample(tile_list, int(len(tile_list) * self.ratio)), 1150)
        super().use(maze)
