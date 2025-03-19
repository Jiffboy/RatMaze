class Item:
    def __init__(self, name, cost, uses=0):
        self.name = name
        self.cost = cost
        self.limited = False if uses == 0 else True
        self.uses_remaining = uses

    def use(self, maze):
        pass

    def can_use(self):
        if self.limited and not self.uses_remaining:
            return False
        return True
