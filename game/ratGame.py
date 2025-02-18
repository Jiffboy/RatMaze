import pygame
from game.scoreboard import Scoreboard
from game.maze import Maze


class RatGame:
    def __init__(self, config):
        self.target = 2
        self.scoreboard = Scoreboard()
        self.maze = Maze(config)

    def do_frame(self):
        self.maze.do_frame()
        self.scoreboard.do_frame()

    def draw(self, screen):
        screen.fill((70, 70, 70))

        self.maze.draw(screen)
        self.scoreboard.draw(screen)

        pygame.display.flip()

    def restart(self):
        self.maze.regenerate_maze(self.maze.end[1])
