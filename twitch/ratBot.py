from twitchio.ext import commands
from vars.globals import chatStats, lock


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
                    chatStats.up += 1
                case "left":
                    chatStats.left += 1
                case "down":
                    chatStats.down += 1
                case "right":
                    chatStats.right += 1
