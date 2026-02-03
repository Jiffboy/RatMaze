from game.items.item import Item


class Random(Item):
    def __init__(self, name, used_by, item):
        self.item = item
        super().__init__(name, used_by)

    def use(self, maze):
        self.item.use(maze)
        super().use(maze)

    def clean_up(self, maze):
        self.item.clean_up(maze)
        super().clean_up(maze)

    def get_log(self):
        item_log = self.item.get_log() if self.item is not None else "Unknown"
        return f"{self.name}: {item_log}"
