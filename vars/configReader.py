import configparser
import os
import math
import json


class ConfigReader:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        # game
        self.init_maze_size = config.getint('game', 'init_maze_size', fallback=7)
        self.vote_threshold = config.getint('game', 'vote_threshold', fallback=2)
        self.debug = config.getboolean('game', 'debug', fallback=False)
        self.countdown_length = config.getint('game', 'countdown_length', fallback=0)
        self.cheese_points = config.getint('game', 'cheese_points', fallback=20)

        # override values if necessary
        if os.path.exists('dev_config.ini'):
            dev_config = configparser.ConfigParser()
            dev_config.read('dev_config.ini')
            self.token = dev_config.get('twitch', 'token', fallback='')
            self.channel = dev_config.get('twitch', 'channel', fallback='')
            self.debug = dev_config.getboolean('game', 'debug', fallback=False)
