import threading
from twitch.chatStats import ChatStats

chat_stats = ChatStats()
lock = threading.Lock()
tile_size = 16