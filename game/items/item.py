class Item:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost
        self.limited = False
        self.uses_remaining = 0

    def use(self, maze):
        pass

    def can_use(self):
        if self.limited and not self.uses_remaining:
            return False
        return True
    