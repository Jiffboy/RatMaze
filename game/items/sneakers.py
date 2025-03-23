from game.items.item import Item


class Sneakers(Item):
    def use(self, maze):
        maze.rat.speed_boost = True
        super().use(maze)

    def clean_up(self, maze):
        maze.rat.speed_boost = False
        super().clean_up(maze)
