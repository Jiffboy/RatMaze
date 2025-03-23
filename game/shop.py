import random

from game.items.itemFactory import ItemFactory


class Shop:
    def __init__(self, config):
        self.config = config
        self.curr_shop = {}
        self.active_items = []
        self.item_factory = ItemFactory(config)
        self.refresh_shop()

    def buy_item(self, item_name):
        self.active_items.append(item_name)

    def use_items(self, maze):
        for item in self.active_items:
            self.curr_shop[item].use(maze)
        self.active_items = []

    def refresh_shop(self):
        self.curr_shop = {}
        item_list = self.item_factory.item_list
        shop_list = random.sample(item_list, min(self.config.item_count, len(item_list)))
        for item in shop_list:
            self.curr_shop[item] = self.item_factory.build(item)

    def can_buy(self, item_name):
        if item_name in self.curr_shop:
            item = self.curr_shop[item_name]
            if item.can_use():
                return True
        return False

    def get_cost(self, item_name):
        if item_name in self.curr_shop:
            return self.curr_shop[item_name].cost
        return 0
