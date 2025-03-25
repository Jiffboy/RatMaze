import random

from game.items.item import Item


class ScatterBomb(Item):
    def __init__(self, name, cost, percent, uses):
        self.percent = percent
        super().__init__(name, cost, uses, sound="resources/audio/skibidi-bop.mp3")

    def use(self, maze):
        tile_list = []

        for curr_x in range(1, maze.width):
            for curr_y in range(1, maze.height):
                tile_list.append((curr_x, curr_y))

        maze.queue_explosion(random.sample(tile_list, int(len(tile_list) * self.percent)), 1150)
        super().use(maze)
