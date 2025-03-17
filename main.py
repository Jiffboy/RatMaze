import pygame
import threading

from vars.configReader import ConfigReader
from twitch.ratBot import RatBot
from game.ratGame import RatGame
from game.items.itemFactory import item_factory
from vars.direction import Direction
from vars.globals import chat_stats, lock, window_width, window_height


# We have to put logic in main because pygame is huffy
def game_thread(config):
    pygame.init()
    game = RatGame(config)
    running = True
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Rat Maze")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            with lock:
                if event.type == pygame.KEYDOWN and config.debug:
                    if event.key == pygame.K_r:
                        chat_stats.reset()
                        game.restart()
                    elif event.key == pygame.K_UP:
                        chat_stats.add_vote(Direction.UP, config.channel)
                        game.force_move(Direction.UP)
                    elif event.key == pygame.K_RIGHT:
                        chat_stats.add_vote(Direction.RIGHT, config.channel)
                        game.force_move(Direction.RIGHT)
                    elif event.key == pygame.K_DOWN:
                        chat_stats.add_vote(Direction.DOWN, config.channel)
                        game.force_move(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        chat_stats.add_vote(Direction.LEFT, config.channel)
                        game.force_move(Direction.LEFT)
                    elif event.key == pygame.K_LEFTBRACKET:
                        game.force_resize_maze(-2)
                    elif event.key == pygame.K_RIGHTBRACKET:
                        game.force_resize_maze(2)
                    elif event.key == pygame.K_1:
                        chat_stats.add_item(item_factory("smallbomb"))
                    elif event.key == pygame.K_2:
                        chat_stats.add_item(item_factory("mediumbomb"))
                    elif event.key == pygame.K_3:
                        chat_stats.add_item(item_factory("largebomb"))

        game.do_frame()
        game.draw(screen)
    pygame.quit()


if __name__ == '__main__':
    # only instantiate configReader once
    config = ConfigReader()

    bot = RatBot(config)
    thread = threading.Thread(target=game_thread, args=[config])
    thread.start()
    bot.run()
