import configparser


class ConfigReader:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        # twitch
        self.token = config.get('twitch', 'token', fallback='')
        self.channel = config.get('twitch', 'channel', fallback='JiffBoy')

        # game
        self.init_width = config.getint('game', 'init_width', fallback=5)
        self.init_height = config.getint('game', 'init_height', fallback=5)
        self.vote_threshold = config.getint('game', 'vote_threshold', fallback=2)
        self.debug = config.getboolean('game', 'debug', fallback=False)
