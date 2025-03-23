from game.items.item import Item


class Shuffle(Item):
    def use(self, maze):
        maze.regenerate_maze((maze.rat.x, maze.rat.y))
        super().use(maze)
