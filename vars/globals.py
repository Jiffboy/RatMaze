import threading
from twitch.chatStats import ChatStats

chat_stats = ChatStats()
lock = threading.Lock()
tile_size = 16
grid_anchor_x = 200
grid_anchor_y = 100
