from game.items.bomb import Bomb
from game.items.scatterbomb import ScatterBomb
from game.items.nuke import Nuke
from game.items.teleporter import Teleporter
from game.items.auxcord import Auxcord
from game.items.drill import Drill
from game.items.random import Random
from game.items.downsize import Downsize
from game.items.crashout import Crashout
from game.items.shuffle import Shuffle
from game.items.airjordans import Airjordans
from game.items.sneakers import Sneakers


class ItemFactory:
    def __init__(self, config):
        self.config = config
        self.item_list = [
            "smallbomb",
            "mediumbomb",
            "largebomb",
            "scatterbomb",
            "nuke",
            "teleporter",
            "auxcord",
            "smalldrill",
            "largedrill",
            "downsize",
            "random",
            "crashout",
            "shuffle",
            "airjordans",
            "sneakers"
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
                return Nuke(item, self.config.nuke_cost, self.config.nuke_stock, "resources/audio/explosion.mp3")
            case "teleporter":
                return Teleporter(item, self.config.teleporter_cost, self.config.teleporter_stock, "resources/audio/boing.mp3")
            case "auxcord":
                return Auxcord(item, self.config.auxcord_cost, self.config.auxcord_stock)
            case "smalldrill":
                return Drill(item, self.config.small_drill_cost, self.config.small_drill_stock, 3)
            case "largedrill":
                return Drill(item, self.config.large_drill_cost, self.config.large_drill_stock, 5)
            case "random":
                return Random(item, self.config.random_cost, self.config.random_stock, self.config.random_exclusions, self)
            case "downsize":
                return Downsize(item, self.config.downsize_cost, self.config.downsize_stock, self.config.downsize_amount)
            case "crashout":
                return Crashout(item, self.config.crashout_cost, self.config.crashout_stock, sound="resources/audio/desk-slamming.mp3")
            case "shuffle":
                return Shuffle(item, self.config.shuffle_cost, self.config.shuffle_stock, sound="resources/audio/cha-cha-real-smooth.mp3")
            case "airjordans":
                return Airjordans(item, self.config.airjordans_cost, self.config.airjordans_stock, sound="resources/audio/lebron-james.mp3")
            case "sneakers":
                return Sneakers(item, self.config.sneakers_cost, self.config.sneakers_stock, sound="resources/audio/deja-vu.mp3")
