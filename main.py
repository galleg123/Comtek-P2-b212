import pygame
import random
import sys
from classes import car
from pygame import (
    image,
    display,
    init,
    event,
    QUIT,
)

import classes


init()
size = width, height = 1920, 1000
screen = display.set_mode(size)


def main():
    Car = car.car
    run = True
    while run and display.get_active():
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

        screen.blit(Car.carImg, (100, 100))
        display.flip()


if __name__ == "__main__":
    main()
