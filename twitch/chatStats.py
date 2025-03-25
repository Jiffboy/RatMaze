import math
import random

import pygame.time

from vars.direction import Direction


class ChatStats:
    def __init__(self, config):
        self.config = config
        self.leaderboard = {}
        # Pair of score, balance
        self.leader_list = []
        self.curr_votes = {
            Direction.UP: [],
            Direction.RIGHT: [],
            Direction.DOWN: [],
            Direction.LEFT: []
        }

        # People who have contributed to the current maze
        self.participants = []
        self.cheese_count = 0
        self.countdown_length = config.countdown_length
        self.timeout = pygame.time.get_ticks() + self.countdown_length * 1000
        self.log = ""

    def full_reset(self):
        self.leaderboard = {}
        self.leader_list = []
        self.cheese_count = 0
        self.reset_votes()

    def reset_votes(self):
        self.curr_votes = {
            Direction.UP: [],
            Direction.RIGHT: [],
            Direction.DOWN: [],
            Direction.LEFT: []
        }

    def add_vote(self, direction, user):
        if user not in self.curr_votes[direction]:
            self.curr_votes[direction].append(user)

    def get_vote_count(self, direction):
        return len(self.curr_votes[direction])

    def can_vote(self, user):
        for dir in self.curr_votes.values():
            if user in dir:
                return False
        return True

    def vote_won(self, direction):
        for user in self.curr_votes[direction]:
            self.give_points(user, 1)
            if user not in self.participants:
                self.participants.append(user)

        self.rebuild_list()
        self.reset_votes()
        self.reset_timeout()

    def give_points(self, user, amount):
        if self.leaderboard.get(user) is not None:
            self.leaderboard[user] = (self.leaderboard[user][0] + amount, self.leaderboard[user][1] + amount)
        else:
            self.leaderboard[user] = (amount, amount)

    def spend_points(self, user, amount):
        if self.leaderboard.get(user) is not None:
            self.leaderboard[user] = (self.leaderboard[user][0], self.leaderboard[user][1] - amount)
            self.rebuild_list()

    def can_afford(self, user, amount):
        if self.leaderboard.get(user) is not None and self.get_balance(user) >= amount:
            return True
        return False

    def rebuild_list(self):
        self.leader_list = sorted(self.leaderboard.items(), key=lambda item: item[1][0], reverse=True)

    def got_cheese(self):
        self.cheese_count += 1
        for user in self.participants:
            self.give_points(user, self.config.cheese_points)
        self.rebuild_list()
        self.participants = []
        self.reset_votes()

    def reset_timeout(self):
        self.timeout = pygame.time.get_ticks() + self.countdown_length * 1000

    def is_time_up(self):
        return pygame.time.get_ticks() >= self.timeout

    def time_remaining(self):
        if self.is_time_up():
            return 1

        time_left = self.timeout - pygame.time.get_ticks()
        return math.ceil(time_left / 1000)

    def get_sorted_directions(self):
        options = {}
        for direction in self.curr_votes:
            count = len(self.curr_votes[direction])
            if count > 0:
                if count not in options:
                    options[count] = []
                options[count].append(direction)
        if len(options) == 0:
            return []

        sorted_groups = sorted(options.items(), key=lambda item: item[0], reverse=True)
        sorted_directions = []
        for group in sorted_groups:
            random.shuffle(group[1])
            sorted_directions.extend(group[1])

        return sorted_directions

    def get_balance(self, name):
        has_balance = name in self.leaderboard
        if has_balance:
            return self.leaderboard[name][1]
        else:
            return 0
