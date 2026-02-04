from pygame import mixer


class Item:
    def __init__(self, name, used_by, sound=''):
        self.name = name
        self.sound = sound
        self.used_by = used_by

    def use(self, maze):
        if self.sound != '':
            mixer.music.load(self.sound)
            mixer.music.play()

    def clean_up(self, maze):
        pass

    def get_formatted_name(self):
        return self.name

    def get_log(self):
        return f"{self.used_by} used {self.get_formatted_name()}"
