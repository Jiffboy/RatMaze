import pygame

from vars.globals import chatStats, lock


class Rat:
    def __init__(self, config):
        self.x = 10
        self.y = 300
        self.size = 60
        self.config = config

    def do_frame(self):
        target = self.config.vote_threshold

        with lock:
            if chatStats.up >= target:
                self.y -= self.size
                chatStats.reset()
            elif chatStats.right >= target:
                self.x += self.size
                chatStats.reset()
            elif chatStats.down >= target:
                self.y += self.size
                chatStats.reset()
            elif chatStats.left >= target:
                self.x -= self.size
                chatStats.reset()

    def draw(self, screen):
        pygame.draw.rect(screen, (150, 150, 150), (self.x, self.y, self.size, self.size))
