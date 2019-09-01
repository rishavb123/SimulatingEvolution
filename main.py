import pygame
import time

from constants import *
from objects import Rect, MovingRect, Player
from environment import Environment

def main():
    pygame.init()

    display = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    env = Environment()
    env.add(Rect(14.3, 40.6, 5.7, 1.3))
    env.add(MovingRect(100, 38, 10, 10, -10, 0))
    env.add(Player(0, 0, 10, 10, 10))

    start_time = time.time()
    last_time = start_time

    while True:
        display.fill(background_color)
        event_queue = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                quit()
            elif event.type == pygame.VIDEORESIZE:
                display = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            else:
                env.handle(event)

        cur_time = time.time()
        env.update(display, cur_time - start_time, cur_time - last_time, True)
        last_time = cur_time

        pygame.display.update()
        time.sleep(1.0 / fps)


if __name__ == '__main__':
    main()