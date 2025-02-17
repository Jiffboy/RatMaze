import pygame
import random
from game.rat import Rat
from game.scoreboard import Scoreboard
from game.maze import Maze


class RatGame:
    def __init__(self, config):
        self.target = 2
        self.rat = Rat(config)
        self.scoreboard = Scoreboard()
        self.maze = Maze(config, 200, 100)

    def do_frame(self):
        self.rat.do_frame()
        self.scoreboard.do_frame()

    def draw(self, screen):
        screen.fill((255, 255, 255))

        self.maze.draw(screen)
        self.rat.draw(screen)
        self.scoreboard.draw(screen)

        pygame.display.flip()

    def restart(self):
        self.maze.regenerate_maze(self.maze.end[1])
