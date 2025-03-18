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
            if chat_stats.can_vote(message.author.name):
                match message.content.lower():
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
        await self.handle_commands(message)

    @commands.command(name='balance')
    async def balance(self, ctx):
        name = ctx.author.name
        msg = f"{name}'s balance: "
        with lock:
            msg += str(chat_stats.get_balance(name))
        await ctx.send(msg)

    @commands.command(name='smallbomb')
    async def smallbomb(self, ctx):
        with lock:
            success = chat_stats.buy_item(ctx.author.name, 'smallbomb')
            if not success:
                await ctx.send(f"Cannot purchase. Current balance: {chat_stats.get_balance(ctx.author.name)}")

    @commands.command(name='mediumbomb')
    async def mediumbomb(self, ctx):
        with lock:
            success = chat_stats.buy_item(ctx.author.name, 'mediumbomb')
            if not success:
                await ctx.send(f"Cannot purchase. Current balance: {chat_stats.get_balance(ctx.author.name)}")

    @commands.command(name='largebomb')
    async def largebomb(self, ctx):
        with lock:
            success = chat_stats.buy_item(ctx.author.name, 'largebomb')
            if not success:
                await ctx.send(f"Cannot purchase. Current balance: {chat_stats.get_balance(ctx.author.name)}")
