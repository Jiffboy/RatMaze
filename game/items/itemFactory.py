from game.items.bomb import Bomb


def item_factory(item):
    match item:
        case "smallbomb":
            return Bomb(1)
        case "mediumbomb":
            return Bomb(2)
        case "largebomb":
            return Bomb(3)
