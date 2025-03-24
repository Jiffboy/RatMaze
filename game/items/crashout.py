from game.items.item import Item


class Crashout(Item):
    def use(self, maze):
        maze.complete_reset()
        super().use(maze)

    def get_log(self):
        return f"{self.name}. Do you feel better?"
