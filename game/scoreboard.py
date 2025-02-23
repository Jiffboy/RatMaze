import pygame

from vars.direction import Direction
from vars.globals import chat_stats, lock, grid_anchor_y


class Scoreboard:
    def __init__(self):
        self.font = pygame.font.SysFont('Comic Sans MS', 20)
        self.line_distance = 40
        self.x_pos = 25
        self.users_to_show = 5

    def do_frame(self):
        pass

    def draw(self, screen):
        with lock:
            line_list = [
                f"Cheeses: {str(chat_stats.cheese_count)}",
                f"Up: {str(chat_stats.get_vote_count(Direction.UP))}",
                f"Left: {str(chat_stats.get_vote_count(Direction.LEFT))}",
                f"Down: {str(chat_stats.get_vote_count(Direction.DOWN))}",
                f"Right: {str(chat_stats.get_vote_count(Direction.RIGHT))}",
                "",
                "Leaderboard"
            ]

            curr_count = 0
            for user in chat_stats.leader_list:
                if curr_count < self.users_to_show:
                    line_list.append(f"{user[0]}: {str(user[1])}")
                    curr_count += 1

            curr_line = 0
            for line in line_list:
                line_surface = self.font.render(line, False, (255, 255, 255))
                screen.blit(line_surface, (self.x_pos, grid_anchor_y + self.line_distance * curr_line))
                curr_line += 1
