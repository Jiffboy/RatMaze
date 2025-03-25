from game.items.item import Item


class Bomb(Item):
    def __init__(self, name, cost, count, size):
        self.size = size
        super().__init__(name, cost, count, sound="resources/audio/vine-boom.mp3")

    def use(self, maze):
        x = maze.rat.get_x()
        y = maze.rat.get_y()
        tile_list = []

        for curr_x in range(x-self.size, x+self.size+1):
            for curr_y in range(y-self.size, y+self.size+1):
                tile_list.append((curr_x, curr_y))

        maze.queue_explosion(tile_list)
        super().use(maze)
