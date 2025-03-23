from pygame import mixer


class Item:
    def __init__(self, name, cost, uses=0, sound=''):
        self.name = name
        self.cost = cost
        self.limited = False if uses == 0 else True
        self.uses_remaining = uses
        self.sound = sound

    def use(self, maze):
        if self.sound != '':
            mixer.music.load(self.sound)
            mixer.music.play()
        self.uses_remaining -= 1

    def can_use(self):
        if self.limited and not self.uses_remaining:
            return False
        return True

    def clean_up(self, maze):
        pass
