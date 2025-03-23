import random

from game.items.item import Item


class Random(Item):
    def __init__(self, name, cost, count, factory):
        self.factory = factory
        self.item = None
        super().__init__(name, cost, count)

    def use(self, maze):
        choice = random.choice(self.factory.item_list)
        item = self.factory.build(choice)
        self.item = item
        item.use(maze)

        super().use(maze)

    def clean_up(self, maze):
        self.item.clean_up(maze)
        super().clean_up(maze)
