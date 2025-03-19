import math
import random

import pygame.time

from vars.direction import Direction
from game.items.itemFactory import ItemFactory


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
        self.cheese_count = 0
        self.countdown_length = config.countdown_length
        self.timeout = pygame.time.get_ticks() + self.countdown_length * 1000
        self.curr_shop = {}
        self.active_items = []
        self.item_factory = ItemFactory(config)
        self.refresh_shop()

    def full_reset(self):
        self.leaderboard = {}
        self.leader_list = []
        self.cheese_count = 0
        self.reset_votes()
        self.refresh_shop()

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

        self.rebuild_list()
        self.reset_votes()
        self.reset_timeout()

    def rebuild_list(self):
        self.leader_list = sorted(self.leaderboard.items(), key=lambda item: item[1][0], reverse=True)

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

    def buy_item(self, name, item_name):
        if item_name in self.curr_shop:
            item = self.curr_shop[item_name]
            if item.can_use() and self.get_balance(name) >= item.cost:
                self.active_items.append(item_name)
                self.leaderboard[name] = (self.leaderboard[name][0], self.leaderboard[name][1] - item.cost)
                self.rebuild_list()
                return True
        return False

    def use_items(self, maze):
        for item in self.active_items:
            self.curr_shop[item].use(maze)
        self.active_items = []

    def refresh_shop(self):
        self.curr_shop = {}
        item_list = self.item_factory.item_list
        shop_list = random.sample(item_list, min(self.config.item_count, len(item_list)))
        for item in shop_list:
            self.curr_shop[item] = self.item_factory.build(item)

    def is_in_shop(self, item_name):
        return item_name in self.curr_shop
