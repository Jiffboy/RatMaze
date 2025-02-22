from twitchio.ext import commands
from vars.direction import Direction
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
            if chat_stats.can_vote(message.author.name):
                match message.content.lower():
                    case "up":
                        chat_stats.add_vote(Direction.UP, message.author.name)
                    case "left":
                        chat_stats.add_vote(Direction.LEFT, message.author.name)
                    case "down":
                        chat_stats.add_vote(Direction.DOWN, message.author.name)
                    case "right":
                        chat_stats.add_vote(Direction.RIGHT, message.author.name)
