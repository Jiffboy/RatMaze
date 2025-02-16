import threading
from twitch.chatStats import ChatStats

chatStats = ChatStats()
lock = threading.Lock()
