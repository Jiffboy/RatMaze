import math
import random

import pygame.time

from vars.direction import Direction


class ChatStats:
    def __init__(self, config):
        self.leaderboard = {}
        # Pair of score, balance
        self.leader_list = []
        self.curr_votes = {
            Direction.UP: [],
            Direction.RIGHT: [],
            Direction.DOWN: [],
            Direction.LEFT: []
        }
        self.cheese_count = 0
        self.countdown_length = config.countdown_length
        self.timeout = pygame.time.get_ticks() + self.countdown_length * 1000
        self.items = []

    def reset(self):
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
            if self.leaderboard.get(user) is not None:
                self.leaderboard[user] = (self.leaderboard[user][0] + 1, self.leaderboard[user][1] + 1)
            else:
                self.leaderboard[user] = (1, 1)
        self.leader_list = sorted(self.leaderboard.items(), key=lambda item: item[1][0], reverse=True)
        self.reset_votes()
        self.reset_timeout()

    def got_cheese(self):
        self.cheese_count += 1

    def reset_timeout(self):
        self.timeout = pygame.time.get_ticks() + self.countdown_length * 1000

    def is_time_up(self):
        return pygame.time.get_ticks() >= self.timeout

    def time_remaining(self):
        if self.is_time_up():
            return 1

        time_left = self.timeout - pygame.time.get_ticks()
        return math.ceil(time_left / 1000)

    def get_random_directions(self):
        options = []
        for direction in self.curr_votes:
            if len(self.curr_votes[direction]) > 0:
                options.append(direction)
        if len(options) == 0:
            return []
        random.shuffle(options)
        return options

    def get_balance(self, name):
        has_balance = name in self.leaderboard
        if has_balance:
            return self.leaderboard[name][1]
        else:
            return 0

    def add_item(self, item):
        self.items.append(item)

    def item_used(self):
        return len(self.items) > 0

    def get_item(self):
        return self.items.pop()

    def spend(self, name, amount):
        self.leaderboard[name] = (self.leaderboard[name][0], self.leaderboard[name][1] - amount)