import threading

from vars.configReader import ConfigReader

# multi-threaded variables
lock = threading.Lock()

# constants
tile_size = 64
grid_size = 857
grid_anchor_x = 531
grid_anchor_y = 123
window_width = 1920
window_height = 1080
frame_rate = 60
server_namespace = "/ratmaze/game"