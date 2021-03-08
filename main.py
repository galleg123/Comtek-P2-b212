import pygame
import random
import sys

from classes import (
    car,
    road,
)
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
    
    Car = car.car()
    Car.rect.centery = Car.rect.centery + 8                                     # Make it start 8 pixels below the top of the screen
    Road = road.road().create(Car.rect.height)
    run = True
    while run and display.get_active():
        screen.fill([255,255,255])
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            Car.movement(event)
        


        Car.rect = Car.rect.move(Car.speed,0)                                   # Move the car
        screen.blit(Road.img, Road.rect)                                        # Render the road
        screen.blit(Car.img, Car.rect)                                          # Render the car
        display.flip()
        



if __name__ == "__main__":
    main()
