import pygame
import random
import sys
from pygame import (
    image,
    display,
    init,
)
#tilfældig linie hej
init()
size = width, height = 1920, 1000
screen = display.set_mode(size)


def main():
    run = True
    while run or display.get_active():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


if __name__ == "__main__":
    main()
