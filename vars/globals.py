import threading
from twitch.chatStats import ChatStats
from vars.configReader import ConfigReader

# variables
chat_stats = ChatStats(ConfigReader())
lock = threading.Lock()

# constants
tile_size = 64
grid_size = 800
grid_anchor_x = 200
grid_anchor_y = 80
window_width = 1200
window_height = 1000
