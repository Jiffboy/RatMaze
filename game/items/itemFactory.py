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
    def build(self, name, user, item_config):
        match name.lower().replace(" ", ""):
            case "smallbomb":
                return Bomb(name, user, 1)
            case "mediumbomb":
                return Bomb(name, user, 2)
            case "largebomb":
                return Bomb(name, user, 3)
            case "scatterbomb":
                return ScatterBomb(name, user, item_config["percent"])
            case "nuke":
                return Nuke(name, user, sound="resources/audio/explosion.mp3")
            case "teleporter":
                return Teleporter(name, user, sound="resources/audio/boing.mp3")
            case "auxcord":
                return Auxcord(name, user)
            case "smalldrill":
                return Drill(name, user, 3)
            case "largedrill":
                return Drill(name, user, 5)
            case "random":
                return Random(name, user, item_config["valid_items"])
            case "downsize":
                return Downsize(name, user, item_config["amount"])
            case "crashout":
                return Crashout(name, user, sound="resources/audio/desk-slamming.mp3")
            case "shuffle":
                return Shuffle(name, user, sound="resources/audio/cha-cha-real-smooth.mp3")
            case "airjordans":
                return Airjordans(name, user, sound="resources/audio/lebron-james.mp3")
            case "sneakers":
                return Sneakers(name, user, sound="resources/audio/deja-vu.mp3")
