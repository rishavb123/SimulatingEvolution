import pygame
import time

from constants import *
from objects import *
from intervals import *
from environment import Environment

def main():
    pygame.init()

    display = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    env = Environment()
    red = Agent(0, 0, 5, 5, 10, color=(255, 0, 0))
    blue = Agent(95, 95, 5, 5, 20, color=(0, 0, 255))
    black = Agent(95, 0, 5, 5, 30, color=(0, 0, 0))
    gray = Agent(0, 95, 5, 5, 40, color=(175, 175, 175))
    yellow = Agent(45, 0, 10, 10, 10, color=(255, 255, 0))
    purple = Agent(0, 45, 10, 10, 20, color=(255, 0, 255))
    orange = Agent(90, 45, 10, 10, 30, color=(255, 165, 0))
    pink = Agent(45, 0, 10, 10, 40, color=(255, 192, 203))
    env.add([red, blue, gray, black, gray, yellow, purple, orange, pink])

    FoodSpawner(lambda: 3, lambda: 3, lambda: 1, 0.5, 0.6, env).start()

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

        print("RED: {} \t BLUE: {} \t BLACK: {} \t GRAY: {} \t YELLOW: {} \t PURPLE: {} \t ORANGE: {} \t PINK: {}".format(int(red.energy), int(blue.energy), int(black.energy), int(gray.energy), int(yellow.energy), int(purple.energy), int(orange.energy), int(pink.energy)))

        pygame.display.update()

        if fps:
            time.sleep(1.0 / fps)


if __name__ == '__main__':
    main()