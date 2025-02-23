import pygame
import threading

from vars.configReader import ConfigReader
from twitch.ratBot import RatBot
from game.ratGame import RatGame
from vars.direction import Direction
from vars.globals import chat_stats, lock


# We have to put logic in main because pygame is huffy
def game_thread(config):
    pygame.init()
    game = RatGame(config)
    running = True
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Rat Maze")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and config.debug:
                if event.key == pygame.K_r:
                    with lock:
                        chat_stats.reset()
                    game.restart()
                if event.key == pygame.K_UP:
                    game.force_move(Direction.UP)
                if event.key == pygame.K_RIGHT:
                    game.force_move(Direction.RIGHT)
                if event.key == pygame.K_DOWN:
                    game.force_move(Direction.DOWN)
                if event.key == pygame.K_LEFT:
                    game.force_move(Direction.LEFT)

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
