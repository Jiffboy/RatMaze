import pygame

from pygame import mixer
from game.ui import UI
from game.maze import Maze
from vars.globals import chat_stats, shop, lock


class RatGame:
    def __init__(self, config):
        self.target = 2
        self.ui = UI()
        self.maze = Maze(config)
        self.base_width = config.init_maze_size
        self.base_height = config.init_maze_size
        self.background_screen = pygame.image.load("resources/images/ui/main_ui.png")
        self.in_animation = False
        mixer.init()

    def do_frame(self):
        if not self.maze.rat.animation_locked:
            with lock:
                if shop.has_items():
                    shop.use_items(self.maze)
                    self.maze.rat.celebrate()
                elif self.maze.has_won():
                    if not self.in_animation:
                        self.maze.eat_cheese()
                        self.in_animation = True
                    else:
                        chat_stats.got_cheese()
                        shop.cleanup_items(self.maze)
                        shop.refresh_shop()
                        self.force_resize_maze(2)
                        self.in_animation = False
        self.maze.do_frame()

    def force_resize_maze(self, size):
        width = max(7, self.maze.width + size)
        height = max(7, self.maze.height + size)
        self.maze.resize_maze(width, height, (1, min(self.maze.end[1], height - 2)))

    def force_regenerate_maze(self):
        self.maze.regenerate_maze((self.maze.rat.get_x(), self.maze.rat.get_y()))

    def draw(self, screen):
        screen.blit(self.background_screen, (0, 0))

        self.maze.draw(screen)
        self.ui.draw(screen)

        pygame.display.flip()

    def restart(self):
        self.maze.complete_reset()
