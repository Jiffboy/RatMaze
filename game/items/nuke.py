from game.items.item import Item


class Nuke(Item):
    def __init__(self, name, cost, uses):
        super().__init__(name, cost, uses, "resources/audio/explosion.mp3")

    def use(self, maze):
        tile_list = []

        for curr_x in range(1, maze.width):
            for curr_y in range(1, maze.height):
                tile_list.append((curr_x, curr_y))

        maze.destroy_tiles(tile_list, 2500)
        self.uses_remaining -= 1
        self.play_sound()
