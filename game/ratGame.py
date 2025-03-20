import pygame

from pygame import mixer
from game.ui import UI
from game.maze import Maze
from vars.globals import chat_stats, lock


class RatGame:
    def __init__(self, config):
        self.target = 2
        self.ui = UI()
        self.maze = Maze(config)
        self.base_width = config.init_maze_size
        self.base_height = config.init_maze_size
        self.background_screen = pygame.image.load("resources/images/ui/main_ui.png")
        mixer.init()

    def do_frame(self):
        with lock:
            chat_stats.use_items(self.maze)
        self.maze.do_frame()
        if self.maze.has_won():
            mixer.music.load("resources/audio/cheese.mp3")
            mixer.music.play()
            with lock:
                chat_stats.got_cheese()
                chat_stats.refresh_shop()
                self.force_resize_maze(2)

    def force_move(self, direction):
        self.maze.move(direction)

    def force_resize_maze(self, size):
        width = max(7, self.maze.width + size)
        height = max(7, self.maze.width + size)
        self.maze.resize_maze(width, height, min(self.maze.end[1], height - 2))

    def draw(self, screen):
        screen.blit(self.background_screen, (0, 0))

        self.maze.draw(screen)
        self.ui.draw(screen)

        pygame.display.flip()

    def restart(self):
        self.maze.regenerate_maze(self.maze.end[1])
