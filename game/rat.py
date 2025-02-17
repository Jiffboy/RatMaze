import pygame

from vars.globals import chat_stats, lock


class Rat:
    def __init__(self, config):
        self.x = 10
        self.y = 300
        self.size = 60
        self.config = config

    def do_frame(self):
        target = self.config.vote_threshold

        with lock:
            if chat_stats.up >= target:
                self.y -= self.size
                chat_stats.reset()
            elif chat_stats.right >= target:
                self.x += self.size
                chat_stats.reset()
            elif chat_stats.down >= target:
                self.y += self.size
                chat_stats.reset()
            elif chat_stats.left >= target:
                self.x -= self.size
                chat_stats.reset()

    def draw(self, screen):
        pygame.draw.rect(screen, (150, 150, 150), (self.x, self.y, self.size, self.size))
