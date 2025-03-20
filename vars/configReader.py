import configparser
import os


class ConfigReader:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        # twitch
        self.token = config.get('twitch', 'token', fallback='')
        self.channel = config.get('twitch', 'channel', fallback='')

        # game
        self.init_maze_size = config.getint('game', 'init_maze_size', fallback=7)
        self.vote_threshold = config.getint('game', 'vote_threshold', fallback=2)
        self.debug = config.getboolean('game', 'debug', fallback=False)
        self.countdown_length = config.getint('game', 'countdown_length', fallback=0)

        # shop
        self.item_count = config.getint('shop', 'item_count', fallback=5)
        self.small_bomb_cost = config.getint('shop', 'small_bomb_cost', fallback=5)
        self.small_bomb_stock = config.getint('shop', 'small_bomb_stock', fallback=0)
        self.medium_bomb_cost = config.getint('shop', 'medium_bomb_cost', fallback=10)
        self.medium_bomb_stock = config.getint('shop', 'medium_bomb_stock', fallback=0)
        self.large_bomb_cost = config.getint('shop', 'large_bomb_cost', fallback=15)
        self.large_bomb_stock = config.getint('shop', 'large_bomb_stock', fallback=0)
        self.scatter_bomb_cost = config.getint('shop', 'scatter_bomb_cost', fallback=30)
        self.scatter_bomb_percent = config.getfloat('shop', 'scatter_bomb_percent', fallback=0.2)
        self.scatter_bomb_stock = config.getint('shop', 'scatter_bomb_stock', fallback=3)
        self.nuke_cost = config.getint('shop', 'nuke_cost', fallback=100)
        self.nuke_stock = config.getint('shop', 'nuke_stock', fallback=1)
        self.teleporter_cost = config.getint('shop', 'teleporter_cost', fallback=50)
        self.teleporter_stock = config.get('shop', 'teleporter_stock', fallback=1)

        # override values if necessary
        if os.path.exists('dev_config.ini'):
            dev_config = configparser.ConfigParser()
            dev_config.read('dev_config.ini')
            self.token = dev_config.get('twitch', 'token', fallback='')
            self.channel = dev_config.get('twitch', 'channel', fallback='')
