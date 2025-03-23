import random

from game.items.item import Item


class Random(Item):
    def __init__(self, name, cost, count, exclusions, factory):
        self.factory = factory
        self.item = None
        self.excluded_items = exclusions
        super().__init__(name, cost, count)

    def use(self, maze):
        item_list = [item for item in self.factory.item_list if item not in self.excluded_items]
        choice = random.choice(item_list)
        item = self.factory.build(choice)
        self.item = item
        item.use(maze)

        super().use(maze)

    def clean_up(self, maze):
        self.item.clean_up(maze)
        super().clean_up(maze)
