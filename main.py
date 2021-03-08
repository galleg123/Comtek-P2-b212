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
    transform,
)

import classes


init()
size = width, height = 1920, 1000
screen = display.set_mode(size)


def main():
    
    Car = car.car
    run = True
    while run and display.get_active():
        screen.fill([255,255,255])
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

        screen.blit(Car.img, Car.rect)
        display.flip()


if __name__ == "__main__":
    main()
