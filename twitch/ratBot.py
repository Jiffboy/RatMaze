import asyncio

from twitchio.ext import commands
from vars.direction import Direction
from vars.globals import chat_stats, shop, lock


class RatBot(commands.Bot):
    def __init__(self, config):
        self.config = config
        super().__init__(
            token=config.token,
            prefix="$",
            initial_channels=[config.channel]
        )

    def run_bot_in_thread(self):
        asyncio.new_event_loop()
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.run()

    async def event_message(self, message):
        with lock:
            text = message.content.lower()
            user = message.author.name
            if chat_stats.can_vote(user):
                match text:
                    case "up" | "north":
                        chat_stats.add_vote(Direction.UP, message.author.name)
                        return
                    case "left" | "west":
                        chat_stats.add_vote(Direction.LEFT, message.author.name)
                        return
                    case "down" | "south":
                        chat_stats.add_vote(Direction.DOWN, message.author.name)
                        return
                    case "right" | "east":
                        chat_stats.add_vote(Direction.RIGHT, message.author.name)
                        return
            if text.startswith('$'):
                item_name = text.replace('$', '')
                if shop.can_buy(item_name):
                    cost = shop.get_cost(item_name)
                    if chat_stats.can_afford(user, cost):
                        shop.buy_item(item_name)
                        chat_stats.spend_points(user, cost)
                        chat_stats.log = f"{user} used {shop.get_log(item_name)}!"
                        return

        await self.handle_commands(message)

    @commands.command(name='balance')
    async def balance(self, ctx):
        name = ctx.author.name
        msg = f"{name}'s balance: "
        with lock:
            msg += str(chat_stats.get_balance(name))
        await ctx.send(msg)
