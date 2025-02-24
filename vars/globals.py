import threading
from twitch.chatStats import ChatStats

chat_stats = ChatStats()
lock = threading.Lock()
tile_size = 64
grid_size = 800
grid_anchor_x = 200
grid_anchor_y = 80
window_width = 1200
window_height = 1000
