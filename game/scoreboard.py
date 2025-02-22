import pygame

from vars.direction import Direction
from vars.globals import chat_stats, lock, grid_anchor_y


class Scoreboard:
    def __init__(self):
        self.font = pygame.font.SysFont('Comic Sans MS', 20)
        self.line_distance = 40

    def do_frame(self):
        pass

    def draw(self, screen):
        with lock:
            up_surface = self.font.render("Up: " + str(chat_stats.get_vote_count(Direction.UP)), False, (255, 255, 255))
            screen.blit(up_surface, (50, grid_anchor_y))

            left_surface = self.font.render("Left: " + str(chat_stats.get_vote_count(Direction.LEFT)), False, (255, 255, 255))
            screen.blit(left_surface, (50, grid_anchor_y + self.line_distance))

            down_surface = self.font.render("Down: " + str(chat_stats.get_vote_count(Direction.DOWN)), False, (255, 255, 255))
            screen.blit(down_surface, (50, grid_anchor_y + self.line_distance * 2))

            right_surface = self.font.render("Right: " + str(chat_stats.get_vote_count(Direction.RIGHT)), False, (255, 255, 255))
            screen.blit(right_surface, (50, grid_anchor_y + self.line_distance * 3))
