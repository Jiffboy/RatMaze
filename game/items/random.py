import random

from game.items.item import Item


class Random(Item):
    def __init__(self, name, cost, count, exclusions, factory):
        item_list = [item for item in factory.item_list if item not in exclusions]
        choice = random.choice(item_list)
        self.item = factory.build(choice)
        super().__init__(name, cost, count)

    def use(self, maze):
        self.item.use(maze)

        super().use(maze)

    def clean_up(self, maze):
        self.item.clean_up(maze)
        super().clean_up(maze)
