from game.items.item import Item


class Airjordans(Item):
    def use(self, maze):
        maze.rat.can_jump = True
        super().use(maze)

    def clean_up(self, maze):
        maze.rat.can_jump = False
        super().clean_up(maze)