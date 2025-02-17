from twitchio.ext import commands
from vars.globals import chat_stats, lock


class RatBot(commands.Bot):
    def __init__(self, config):
        super().__init__(
            token=config.token,
            prefix="",
            initial_channels=[config.channel]
        )

    async def event_message(self, message):
        print(f"{message.author.name}: {message.content}")
        with lock:
            match message.content.lower():
                case "up":
                    chat_stats.up += 1
                case "left":
                    chat_stats.left += 1
                case "down":
                    chat_stats.down += 1
                case "right":
                    chat_stats.right += 1
