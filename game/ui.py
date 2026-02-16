import pygame
import time
import math

from vars.direction import Direction
from vars.globals import lock


class UI:
    def __init__(self, server_interface, log_manager):
        self.users_to_show = 10
        self.font_color = (0, 0, 0)
        self.server_interface = server_interface
        self.log_manager = log_manager

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
        self.lb_name_max_chars = 18
        self.lb_line_spacing = 5
        self.lb_font = pygame.font.Font('resources/fonts/FertigoPro-Regular.otf', self.lb_size)

        # timer
        self.timer_width = 1689
        self.timer_height = 37
        self.timer_size = 65
        self.timer_font = pygame.font.Font('resources/fonts/FertigoPro-Regular.otf', self.timer_size)

        # cheese
        self.cheese_width_midpoint = 337
        self.cheese_height_midpoint = 65
        self.cheese_size = 60
        self.cheese_font = pygame.font.Font('resources/fonts/FertigoPro-Regular.otf', self.cheese_size)

        # Ticker
        self.log_height = 470
        self.log_width = 1460
        self.log_size = 20
        self.log_spacing = 5
        self.log_font = pygame.font.Font('resources/fonts/FertigoPro-Regular.otf', self.log_size)

    def draw(self, screen):
        self.draw_leaderboard(screen)
        self.draw_directions(screen)
        self.draw_timer(screen)
        self.draw_cheese(screen)
        self.draw_logs(screen)

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
            curr_point = self.server_interface.next_turn - time.time()
            end_point = self.server_interface.next_turn - self.server_interface.curr_turn
            if end_point != 0:
                percent = max(curr_point / end_point, 0)
            else:
                percent = 0
            if percent > 0:
                rect = pygame.Rect((self.timer_width, self.timer_height), (self.timer_size, self.timer_size))
                top = -math.pi / 2
                draw_thick_arc(screen, self.font_color, rect, top, (math.pi * 2 * percent) + top, 20)

    def draw_cheese(self, screen):
        with lock:
            text = self.cheese_font.render(str(self.server_interface.cheese_count), False, self.font_color)
            text_rect = text.get_rect(center=(self.cheese_width_midpoint, self.cheese_height_midpoint))
            screen.blit(text, text_rect)

    def draw_logs(self, screen):
        with lock:
            y = self.log_height
            for log in self.log_manager.get_logs():
                text = self.log_font.render(log, False, (255, 255, 255))
                screen.blit(text, (self.log_width, y))
                y += self.log_size + self.log_spacing

# I have shamelessly stolen this function from a forum online
def draw_thick_arc(surface, color, rect, start_angle, stop_angle, width, segments=100):
    """Draw a thick arc using polygon approximation"""
    width = min(width, rect.height // 2)  # Ensure width doesn't exceed half the height

    # Calculate inner and outer radii
    outer_radius = min(rect.width, rect.height) // 2
    inner_radius = outer_radius - width

    # Calculate center point
    center_x = rect.centerx
    center_y = rect.centery

    # Convert angles from radians (pygame uses radians for draw.arc)
    start_angle_rad = start_angle
    stop_angle_rad = stop_angle

    # Calculate angle step
    angle_step = (stop_angle_rad - start_angle_rad) / segments

    # Generate points for outer and inner arcs
    points = []

    # Outer arc points (clockwise)
    for i in range(segments + 1):
        angle = start_angle_rad + i * angle_step
        x = center_x + outer_radius * math.cos(angle)
        y = center_y + outer_radius * math.sin(angle)
        points.append((x, y))

    # Inner arc points (counter-clockwise)
    for i in range(segments + 1):
        angle = stop_angle_rad - i * angle_step
        x = center_x + inner_radius * math.cos(angle)
        y = center_y + inner_radius * math.sin(angle)
        points.append((x, y))

    # Draw the polygon
    if len(points) > 2:
        pygame.draw.polygon(surface, color, points)