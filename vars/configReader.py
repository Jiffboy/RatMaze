import configparser


class ConfigReader:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        # twitch
        self.token = config.get('twitch', 'token', fallback='')
        self.channel = config.get('twitch', 'channel', fallback='JiffBoy')

        # game
        self.init_maze_size = config.getint('game', 'init_maze_size', fallback=7)
        self.vote_threshold = config.getint('game', 'vote_threshold', fallback=2)
        self.debug = config.getboolean('game', 'debug', fallback=False)
        self.countdown_length = config.getint('game', 'countdown_length', fallback=0)

        # shop
        self.small_bomb_cost = config.getint('shop', 'small_bomb_cost', fallback=5)
        self.medium_bomb_cost = config.getint('shop', 'medium_bomb_cost', fallback=10)
        self.large_bomb_cost = config.getint('shop', 'large_bomb_cost', fallback=15)
