from twitchio.ext import commands
from vars.direction import Direction
from vars.globals import chat_stats, lock


class RatBot(commands.Bot):
    def __init__(self, config):
        self.config = config
        super().__init__(
            token=config.token,
            prefix="$",
            initial_channels=[config.channel]
        )

    async def event_message(self, message):
        with lock:
            text = message.content.lower()
            user = message.author.name
            if chat_stats.can_vote(user):
                match text:
                    case "up":
                        chat_stats.add_vote(Direction.UP, message.author.name)
                        return
                    case "left":
                        chat_stats.add_vote(Direction.LEFT, message.author.name)
                        return
                    case "down":
                        chat_stats.add_vote(Direction.DOWN, message.author.name)
                        return
                    case "right":
                        chat_stats.add_vote(Direction.RIGHT, message.author.name)
                        return
            if text.startswith('$'):
                if chat_stats.buy_item(user, text.replace('$', '')):
                    return
        await self.handle_commands(message)

    @commands.command(name='balance')
    async def balance(self, ctx):
        name = ctx.author.name
        msg = f"{name}'s balance: "
        with lock:
            msg += str(chat_stats.get_balance(name))
        await ctx.send(msg)
