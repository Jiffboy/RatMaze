import pygame

from vars.direction import Direction
from vars.globals import chat_stats, lock


class UI:
    def __init__(self):
        self.users_to_show = 10
        self.font_color = (0, 0, 0)

        # direction tally
        self.dt_line_diff = 45
        self.dt_midpoint = 1688
        self.dt_size = 40
        self.dt_height = 248
        self.dt_line_spacing = 5
        self.dt_font = pygame.font.Font('resources/fonts/FertigoPro-Regular.otf', self.dt_size)

        # leaderboard
        self.lb_line_diff = 45
        self.lb_size = 30
        self.lb_height = 239
        self.lb_width = 112
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

    def draw(self, screen):
        self.draw_leaderboard(screen)
        self.draw_directions(screen)
        self.draw_timer(screen)
        self.draw_cheese(screen)

    def draw_leaderboard(self, screen):
        with lock:
            curr_line = 0
            for user in chat_stats.leader_list:
                if curr_line >= self.users_to_show:
                    return
                line_surface = self.lb_font.render(f"{user[0]}: {str(user[1][0])}", False, (0, 0, 0))
                x = self.lb_width
                y = self.lb_height - self.lb_size + (curr_line * self.lb_line_diff) - self.lb_line_spacing
                screen.blit(line_surface, (x, y))
                curr_line += 1

    def draw_directions(self, screen):
        with lock:
            directions = [
                str(chat_stats.get_vote_count(Direction.LEFT)),
                str(chat_stats.get_vote_count(Direction.UP)),
                str(chat_stats.get_vote_count(Direction.RIGHT)),
                str(chat_stats.get_vote_count(Direction.DOWN))
            ]
            curr_line = 0
            for dir in directions:
                line_surface = self.dt_font.render(dir, False, (0, 0, 0))
                x = self.dt_midpoint - (self.dt_size / 4)
                y = self.dt_height - self.dt_size + (curr_line * self.dt_line_diff) - self.dt_line_spacing
                screen.blit(line_surface, (x, y))
                curr_line += 1

    def draw_timer(self, screen):
        with lock:
            text = self.timer_font.render(str(chat_stats.time_remaining()), False, self.font_color)
            text_rect = text.get_rect(center=(self.timer_width_midpoint, self.timer_height_midpoint))
            screen.blit(text, text_rect)

    def draw_cheese(self, screen):
        with lock:
            text = self.cheese_font.render(str(chat_stats.cheese_count), False, self.font_color)
            text_rect = text.get_rect(center=(self.cheese_width_midpoint, self.cheese_height_midpoint))
            screen.blit(text, text_rect)
