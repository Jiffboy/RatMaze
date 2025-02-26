import pygame

from pygame import mixer
from game.scoreboard import Scoreboard
from game.maze import Maze
from vars.globals import chat_stats, lock


class RatGame:
    def __init__(self, config):
        self.target = 2
        self.scoreboard = Scoreboard()
        self.maze = Maze(config)
        self.base_width = config.init_width
        self.base_height = config.init_height
        mixer.init()
        mixer.music.load("resources/audio/cheese.mp3")

    def do_frame(self):
        self.maze.do_frame()
        self.scoreboard.do_frame()
        if self.maze.has_won():
            mixer.music.play()
            with lock:
                chat_stats.got_cheese()
                self.force_resize_maze(2)

    def force_move(self, direction):
        self.maze.move(direction)

    def force_resize_maze(self, size):
        width = self.maze.width + size
        height = self.maze.width + size
        self.maze.resize_maze(width, height, self.maze.end[1])

    def draw(self, screen):
        screen.fill((70, 70, 70))

        self.maze.draw(screen)
        self.scoreboard.draw(screen)

        pygame.display.flip()

    def restart(self):
        self.maze.regenerate_maze(self.maze.end[1])
