import configparser


class ConfigReader:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        # twitch
        self.token = config.get('twitch', 'token', fallback='')
        self.channel = config.get('twitch', 'channel', fallback='JiffBoy')

        # game
        self.grid_width = config.getint('game', 'grid_width', fallback=2)
        self.grid_height = config.getint('game', 'grid_height', fallback=2)
        self.vote_threshold = config.getint('game', 'vote_threshold', fallback=2)
