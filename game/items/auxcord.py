import random
import os
from pygame import mixer

from game.items.item import Item


class Auxcord(Item):
    def use(self, maze):
        options = os.listdir('resources/audio/auxcord')
        if len(options) > 0:
            chosen = random.choice(options)
            mixer.music.load(f"resources/audio/auxcord/{chosen}")
            mixer.music.play()

        super().use(maze)
