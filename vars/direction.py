from enum import Enum


class Direction(Enum):
    UP = "up"
    RIGHT = "right"
    DOWN = "down"
    LEFT = "left"
    NONE = "none"

    def get_xy(self):
        match self:
            case Direction.UP:
                return 0, -1
            case Direction.RIGHT:
                return 1, 0
            case Direction.DOWN:
                return 0, 1
            case Direction.LEFT:
                return -1, 0
            case Direction.NONE:
                return 0, 0
