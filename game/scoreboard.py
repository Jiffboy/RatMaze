import pygame

from vars.globals import chat_stats, lock


class Scoreboard:
    def __init__(self):
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

    def do_frame(self):
        pass

    def draw(self, screen):
        with lock:
            up_surface = self.font.render("Up: " + str(chat_stats.up), False, (0, 0, 0))
            screen.blit(up_surface, (10, 0))

            left_surface = self.font.render("Left: " + str(chat_stats.left), False, (0, 0, 0))
            screen.blit(left_surface, (10, 40))

            down_surface = self.font.render("Down: " + str(chat_stats.down), False, (0, 0, 0))
            screen.blit(down_surface, (10, 80))

            right_surface = self.font.render("Right: " + str(chat_stats.right), False, (0, 0, 0))
            screen.blit(right_surface, (10, 120))
