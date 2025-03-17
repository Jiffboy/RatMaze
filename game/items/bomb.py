from game.items.item import Item


class Bomb(Item):
    def __init__(self, size):
        self.size = size

    def use(self, maze):
        x = maze.rat.x
        y = maze.rat.y

        for curr_x in range(x-self.size, x+self.size+1):
            if 0 <= curr_x < maze.width:
                for curr_y in range(y-self.size, y+self.size+1):
                    if 0 <= curr_y < maze.height:
                        tile = maze.grid[curr_x][curr_y]
                        if not tile.is_border and tile.is_wall:
                            tile.set_path()
        maze.build_surface()
