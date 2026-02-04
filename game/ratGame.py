import pygame

from pygame import mixer
from game.ui import UI
from game.maze import Maze
from vars.globals import lock
from vars.direction import Direction
from game.logManager import LogManager


class RatGame:
    def __init__(self, config, server_interface):
        self.target = 2
        self.log_manager = LogManager()
        self.ui = UI(server_interface, self.log_manager)
        self.maze = Maze(config, server_interface)
        self.server_interface = server_interface
        self.base_width = config.init_maze_size
        self.base_height = config.init_maze_size
        self.background_screen = pygame.image.load("resources/images/ui/main_ui.png")
        self.items_used = []
        self.walking = False
        self.eating = False
        self.start_round(False)
        mixer.init()

    def do_frame(self):
        if not self.maze.rat.animation_locked:
            with lock:
                if len(self.server_interface.items_to_use) > 0:
                    self.use_items(self.server_interface.items_to_use)
                    self.server_interface.items_to_use = []
                    self.maze.rat.celebrate()
                elif self.maze.has_won():
                    if not self.eating:
                        self.maze.eat_cheese()
                        self.eating = True
                    else:
                        self.cleanup_items()
                        self.force_resize_maze(2)
                        self.eating = False
                        self.walking = False
                        self.start_round(True)
                elif self.server_interface.move_issued != Direction.NONE:
                    self.maze.move(self.server_interface.move_issued)
                    self.log_manager.add_log(f"Rat moved {self.server_interface.move_issued.to_str()}")
                    self.server_interface.move_issued = Direction.NONE
                    self.walking = True
                elif self.walking:
                    self.walking = False
                    self.start_round(False)
        self.maze.do_frame()

    def start_round(self, got_cheese):
        dir_map = {
            Direction.UP: self.maze.can_move(Direction.UP),
            Direction.RIGHT: self.maze.can_move(Direction.RIGHT),
            Direction.DOWN: self.maze.can_move(Direction.DOWN),
            Direction.LEFT: self.maze.can_move(Direction.LEFT)
        }
        self.server_interface.start_round(got_cheese, dir_map)

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
        self.cleanup_items()

    def use_items(self, items):
        for item in items:
            item.use(self.maze)
            self.log_manager.add_log(item.get_log())
            self.items_used.append(item)

    def cleanup_items(self):
        for item in self.items_used:
            item.clean_up(self.maze)
        self.items_used = []
