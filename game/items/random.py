import random

from game.items.item import Item


class Random(Item):
    def __init__(self, name, cost, count, exclusions, factory):
        self.factory = factory
        self.item = None
        self.item_list = [item for item in self.factory.item_list if item not in exclusions]
        super().__init__(name, cost, count)

    def set_up(self):
        choice = random.choice(self.item_list)
        self.item = self.factory.build(choice)

    def use(self, maze):
        self.item.use(maze)

        super().use(maze)

    def clean_up(self, maze):
        self.item.clean_up(maze)
        super().clean_up(maze)

    def get_log(self):
        item_log = self.item.get_log() if self.item is not None else "Unknown"
        return f"{self.name}: {item_log}"
