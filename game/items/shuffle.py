from game.items.item import Item


class Shuffle(Item):
    def use(self, maze):
        maze.regenerate_maze((maze.rat.get_x(), maze.rat.get_y()))
        super().use(maze)
