import pygame
import time
import math

from vars.direction import Direction
from vars.globals import lock


class UI:
    def __init__(self, server_interface):
        self.users_to_show = 10
        self.font_color = (0, 0, 0)
        self.server_interface = server_interface

        # direction tally
        self.dt_line_diff = 45
        self.dt_midpoint = 1688
        self.dt_size = 40
        self.dt_height = 248
        self.dt_line_spacing = 5
        self.dt_font = pygame.font.Font('resources/fonts/FertigoPro-Regular.otf', self.dt_size)

        # leaderboard
        self.lb_line_diff = 45
        self.lb_size = 25
        self.lb_height = 239
        self.lb_score_width = 112
        self.lb_name_width = 164
        self.lb_name_max_chars = 14
        self.lb_line_spacing = 5
        self.lb_font = pygame.font.Font('resources/fonts/FertigoPro-Regular.otf', self.lb_size)

        # timer
        self.timer_width_midpoint = 1720
        self.timer_height_midpoint = 65
        self.timer_size = 60
        self.timer_font = pygame.font.Font('resources/fonts/FertigoPro-Regular.otf', self.timer_size)

        # cheese
        self.cheese_width_midpoint = 337
        self.cheese_height_midpoint = 65
        self.cheese_size = 60
        self.cheese_font = pygame.font.Font('resources/fonts/FertigoPro-Regular.otf', self.cheese_size)

        # Ticker
        self.log_height = 1010
        self.log_midpoint = 267
        self.log_size = 20
        self.log_font = pygame.font.Font('resources/fonts/FertigoPro-Regular.otf', self.log_size)

    def draw(self, screen):
        self.draw_leaderboard(screen)
        self.draw_directions(screen)
        self.draw_timer(screen)
        self.draw_cheese(screen)
        # self.draw_log(screen)

    def draw_leaderboard(self, screen):
        with lock:
            curr_line = 0
            for user in self.server_interface.leaderboard:
                if curr_line >= self.users_to_show:
                    return
                y = self.lb_height - self.lb_size + (curr_line * self.lb_line_diff) - self.lb_line_spacing
                name = user["username"] \
                    if len(user["username"]) <= self.lb_name_max_chars \
                    else user["username"][:self.lb_name_max_chars] + "..."
                score_surface = self.lb_font.render(f"{str(user['points'])}", False, self.font_color)
                name_surface = self.lb_font.render(name, False, self.font_color)

                screen.blit(score_surface, (self.lb_score_width, y))
                screen.blit(name_surface, (self.lb_name_width, y))
                curr_line += 1

    def draw_directions(self, screen):
        with lock:
            directions = [
                str(self.server_interface.votes[Direction.LEFT]),
                str(self.server_interface.votes[Direction.UP]),
                str(self.server_interface.votes[Direction.RIGHT]),
                str(self.server_interface.votes[Direction.DOWN])
            ]
            curr_line = 0
            for dir in directions:
                line_surface = self.dt_font.render(dir, False, self.font_color)
                x = self.dt_midpoint - (self.dt_size / 4)
                y = self.dt_height - self.dt_size + (curr_line * self.dt_line_diff) - self.dt_line_spacing
                screen.blit(line_surface, (x, y))
                curr_line += 1

    def draw_timer(self, screen):
        with lock:
            number = max(math.ceil(self.server_interface.next_turn - time.time()), 0)
            text = self.timer_font.render(str(number), False, self.font_color)
            text_rect = text.get_rect(center=(self.timer_width_midpoint, self.timer_height_midpoint))
            screen.blit(text, text_rect)

    def draw_cheese(self, screen):
        with lock:
            text = self.cheese_font.render(str(self.server_interface.cheese_count), False, self.font_color)
            text_rect = text.get_rect(center=(self.cheese_width_midpoint, self.cheese_height_midpoint))
            screen.blit(text, text_rect)

    '''
    def draw_log(self, screen):
        with lock:
            text = self.log_font.render(str(chat_stats.log), False, (255, 255, 255))
            text_rect = text.get_rect(center=(self.log_midpoint, self.log_height))
            screen.blit(text, text_rect) 
    '''
