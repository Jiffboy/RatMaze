import pygame

from vars.globals import chat_stats, lock


class Scoreboard:
    def __init__(self):
        self.font = pygame.font.SysFont('Comic Sans MS', 20)

    def do_frame(self):
        pass

    def draw(self, screen):
        with lock:
            up_surface = self.font.render("Up: " + str(chat_stats.up), False, (255, 255, 255))
            screen.blit(up_surface, (50, 200))

            left_surface = self.font.render("Left: " + str(chat_stats.left), False, (255, 255, 255))
            screen.blit(left_surface, (50, 240))

            down_surface = self.font.render("Down: " + str(chat_stats.down), False, (255, 255, 255))
            screen.blit(down_surface, (50, 280))

            right_surface = self.font.render("Right: " + str(chat_stats.right), False, (255, 255, 255))
            screen.blit(right_surface, (50, 320))
