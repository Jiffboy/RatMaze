from game.items.item import Item


class Crashout(Item):
    def use(self, maze):
        maze.complete_reset()
        super().use(maze)
