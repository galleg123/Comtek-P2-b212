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
numOfRoads = 0

def main():
    
    Car = car.car()
    Car.rect.centery = Car.rect.centery + 6                                     # Make it start 6 pixels below the top of the screen
    
    Road = road.road().create(Car.rect.height)
    run = True
    while run and display.get_active():
        
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            Car.movement(event)


        screen.fill([0,0,0])
        Car.rect = Car.rect.move(Car.speed,0)                                   # Move the car

        global numOfRoads
        while ((Road.rect.y + Road.rect.height) <= 1000):                       # Render the road
            screen.blit(Road.img, Road.rect)
            Road.rect.y += (Road.rect.height + 10)
            numOfRoads += 1
        Car.outOfBounds(width, numOfRoads)
        numOfRoads = 0
        Road.rect.y = 0


        
        screen.blit(Car.img, Car.rect)                                          # Render the car
        
        
        display.flip()


if __name__ == "__main__":
    main()