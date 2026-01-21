from game.items.item import Item


class Downsize(Item):
    def __init__(self, name, used_by, amount):
        self.amount = amount
        super().__init__(name, used_by, sound="resources/audio/shrink-ray.mp3")

    def clean_up(self, maze):
        # 5 instead of 7 since it will be increased
        width = max(5, maze.width - self.amount)
        height = max(5, maze.width - self.amount)

        maze.width = width
        maze.height = height

        super().clean_up(maze)
