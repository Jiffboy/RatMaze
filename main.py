import pygame
import threading
import random

from vars.configReader import ConfigReader
from server.serverInterface import ServerInterface
from game.ratGame import RatGame
from vars.globals import lock, window_width, window_height, frame_rate


# We have to put logic in main because pygame is huffy
def run_game(config, server_interface):
    pygame.init()
    game = RatGame(config, server_interface)
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
                    elif event.key == pygame.K_LEFTBRACKET:
                        game.force_resize_maze(-2)
                    elif event.key == pygame.K_RIGHTBRACKET:
                        game.force_resize_maze(2)

        game.do_frame()
        game.draw(screen)
    pygame.quit()


def get_debug_user():
    return f"Test{random.randint(0, 10000)}"


if __name__ == '__main__':
    # only instantiate configReader once
    config = ConfigReader()
    server_interface = ServerInterface()

    thread = threading.Thread(
        target=server_interface.start_client,
        daemon=True
    )
    thread.start()
    server_interface.connected_event.wait()
    run_game(config, server_interface)
