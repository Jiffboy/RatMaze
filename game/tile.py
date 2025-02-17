

class Tile:
    def __init__(self):
        self.is_path = False
        self.is_wall = True
        self.is_start = False
        self.is_end = False

    def set_wall(self):
        self.is_path = False
        self.is_wall = True

    def set_path(self):
        self.is_wall = False
        self.is_path = True

    def set_start(self):
        self.is_path = True
        self.is_start = True

    def set_end(self):
        self.is_path = True
        self.is_end = True
