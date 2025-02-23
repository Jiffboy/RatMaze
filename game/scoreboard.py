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
            up_surface = self.font.render("Up: " + str(chat_stats.get_vote_count(Direction.UP)), False, (255, 255, 255))
            screen.blit(up_surface, (self.x_pos, grid_anchor_y))

            left_surface = self.font.render("Left: " + str(chat_stats.get_vote_count(Direction.LEFT)), False, (255, 255, 255))
            screen.blit(left_surface, (self.x_pos, grid_anchor_y + self.line_distance))

            down_surface = self.font.render("Down: " + str(chat_stats.get_vote_count(Direction.DOWN)), False, (255, 255, 255))
            screen.blit(down_surface, (self.x_pos, grid_anchor_y + self.line_distance * 2))

            right_surface = self.font.render("Right: " + str(chat_stats.get_vote_count(Direction.RIGHT)), False, (255, 255, 255))
            screen.blit(right_surface, (self.x_pos, grid_anchor_y + self.line_distance * 3))

            leaderboard_surface = self.font.render("Leaderboard", False, (255, 255, 255))
            screen.blit(leaderboard_surface, (self.x_pos, grid_anchor_y + self.line_distance * 5))

            curr_line = 6
            for user in chat_stats.leader_list:
                if curr_line + self.users_to_show < 11:
                    user_surface = self.font.render(f"{user[0]}: {str(user[1])}", False, (255, 255, 255))
                    screen.blit(user_surface, (self.x_pos, grid_anchor_y + self.line_distance * curr_line))
                curr_line += 1
