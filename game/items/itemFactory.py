from game.items.bomb import Bomb
from game.items.scatterbomb import ScatterBomb
from game.items.nuke import Nuke
from game.items.teleporter import Teleporter


class ItemFactory:
    def __init__(self, config):
        self.config = config
        self.item_list = [
            "smallbomb",
            "mediumbomb",
            "largebomb",
            "scatterbomb",
            "nuke",
            "teleporter"
        ]

    def build(self, item):
        match item:
            case "smallbomb":
                return Bomb(item, self.config.small_bomb_cost, self.config.small_bomb_stock, 1)
            case "mediumbomb":
                return Bomb(item, self.config.medium_bomb_cost, self.config.small_bomb_stock, 2)
            case "largebomb":
                return Bomb(item, self.config.large_bomb_cost, self.config.small_bomb_stock, 3)
            case "scatterbomb":
                return ScatterBomb(item, self.config.scatter_bomb_cost, self.config.scatter_bomb_percent, self.config.scatter_bomb_stock)
            case "nuke":
                return Nuke(item, self.config.nuke_cost, self.config.nuke_stock)
            case "teleporter":
                return Teleporter(item, self.config.teleporter_cost, self.config.teleporter_stock)

