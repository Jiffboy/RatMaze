from game.items.bomb import Bomb
from game.items.scatterbomb import ScatterBomb


class ItemFactory:
    def __init__(self, config):
        self.config = config
        self.item_list = [
            "smallbomb",
            "mediumbomb",
            "largebomb",
            "scatterbomb"
        ]

    def build(self, item):
        match item:
            case "smallbomb":
                return Bomb(item, self.config.small_bomb_cost, 1)
            case "mediumbomb":
                return Bomb(item, self.config.medium_bomb_cost, 2)
            case "largebomb":
                return Bomb(item, self.config.large_bomb_cost, 3)
            case "scatterbomb":
                return ScatterBomb(item, self.config.scatter_bomb_cost, self.config.scatter_bomb_percent)

