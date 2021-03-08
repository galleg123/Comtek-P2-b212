import pygame
import random
import sys
from pygame import (
    image,
    display,
    init,
)
<<<<<<< HEAD
#tilfældig linie hej ok
=======
#tilfældig linie hejfdfdf
>>>>>>> 6816e3b6158f5104c156e55de39b34608ea9cbc3
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
