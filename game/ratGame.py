import pygame
from game.rat import Rat
from game.scoreboard import Scoreboard


class RatGame:
    def __init__(self, config):
        self.target = 2
        self.rat = Rat(config)
        self.scoreboard = Scoreboard()

    def do_frame(self):
        self.rat.do_frame()
        self.scoreboard.do_frame()

    def draw(self, screen):
        screen.fill((255, 255, 255))

        self.rat.draw(screen)
        self.scoreboard.draw(screen)

        pygame.display.flip()
