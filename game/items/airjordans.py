from game.items.item import Item


class Airjordans(Item):
    def use(self, maze):
        maze.rat.jumping = True
        super().use(maze)

    def clean_up(self, maze):
        maze.rat.jumping = False
        super().clean_up(maze)