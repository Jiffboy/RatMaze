import pygame
import threading

from vars.configReader import ConfigReader
from twitch.ratBot import RatBot
from game.ratGame import RatGame
from vars.direction import Direction
from vars.globals import chat_stats, shop, lock, window_width, window_height, frame_rate


# We have to put logic in main because pygame is huffy
def run_game(config):
    pygame.init()
    game = RatGame(config)
    running = True
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Rat Maze")
    clock = pygame.time.Clock()

    while running:
        # Fixed frame rate
        clock.tick(frame_rate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            with lock:
                if event.type == pygame.KEYDOWN and config.debug:
                    if event.key == pygame.K_r:
                        game.force_regenerate_maze()
                    elif event.key == pygame.K_c:
                        game.restart()
                    elif event.key == pygame.K_s:
                        shop.refresh_shop()
                    elif event.key == pygame.K_UP:
                        chat_stats.add_vote(Direction.UP, config.channel)
                        chat_stats.timeout = pygame.time.get_ticks()
                    elif event.key == pygame.K_RIGHT:
                        chat_stats.add_vote(Direction.RIGHT, config.channel)
                        chat_stats.timeout = pygame.time.get_ticks()
                    elif event.key == pygame.K_DOWN:
                        chat_stats.add_vote(Direction.DOWN, config.channel)
                        chat_stats.timeout = pygame.time.get_ticks()
                    elif event.key == pygame.K_LEFT:
                        chat_stats.add_vote(Direction.LEFT, config.channel)
                        chat_stats.timeout = pygame.time.get_ticks()
                    elif event.key == pygame.K_LEFTBRACKET:
                        game.force_resize_maze(-2)
                    elif event.key == pygame.K_RIGHTBRACKET:
                        game.force_resize_maze(2)
                    elif event.key == pygame.K_KP0:
                        chat_stats.give_points(config.channel, 100)
                        chat_stats.rebuild_list()
                    elif event.key == pygame.K_1:
                        debug_buy(config.channel, list(shop.curr_shop)[0])
                    elif event.key == pygame.K_2:
                        debug_buy(config.channel, list(shop.curr_shop)[1])
                    elif event.key == pygame.K_3:
                        debug_buy(config.channel, list(shop.curr_shop)[2])
                    elif event.key == pygame.K_4:
                        debug_buy(config.channel, list(shop.curr_shop)[3])
                    elif event.key == pygame.K_5:
                        debug_buy(config.channel, list(shop.curr_shop)[4])

        game.do_frame()
        game.draw(screen)
    pygame.quit()


def debug_buy(user, item_name):
    if shop.can_buy(item_name):
        cost = shop.get_cost(item_name)
        if chat_stats.can_afford(user, cost):
            shop.buy_item(item_name)
            chat_stats.spend_points(user, cost)
            chat_stats.log = f"{user} used {shop.get_log(item_name)}!"


if __name__ == '__main__':
    # only instantiate configReader once
    config = ConfigReader()
    bot = RatBot(config)

    thread = threading.Thread(target=bot.run_bot_in_thread)
    thread.daemon = True
    thread.start()

    run_game(config)
