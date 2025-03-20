from game.items.item import Item


class Drill(Item):
    def __init__(self, name, cost, count, size):
        self.size = size
        super().__init__(name, cost, count)

    def use(self, maze):
        x = maze.rat.x
        y = maze.rat.y
        tile_list = []

        for curr_x in range(x + 1, x + self.size + 1):
            tile_list.append((curr_x, y))

        maze.destroy_tiles(tile_list)
        super().use(maze)
