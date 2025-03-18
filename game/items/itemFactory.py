from game.items.bomb import Bomb


class ItemFactory:
    def __init__(self, config):
        self.config = config
        self.item_list = [
            "smallbomb",
            "mediumbomb",
            "largebomb"
        ]

    def build(self, item):
        match item:
            case "smallbomb":
                return Bomb(item, self.config.small_bomb_cost, 1)
            case "mediumbomb":
                return Bomb(item, self.config.medium_bomb_cost, 2)
            case "largebomb":
                return Bomb(item, self.config.large_bomb_cost, 3)

