from game.items.item import Item


class Nuke(Item):
    def use(self, maze):
        tile_list = []

        for curr_x in range(1, maze.width):
            for curr_y in range(1, maze.height):
                tile_list.append((curr_x, curr_y))

        maze.queue_explosion(tile_list, 2500)
        super().use(maze)

    def get_log(self):
        return "A NUKE!!!!!!"
