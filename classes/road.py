import sys
from pygame import (
    image,
    display,
    init,
    event,
    QUIT,
    transform,
)
from classes import car


class road:
    img = image.load("assets\\road.png")                    #Load image of road
    rect = img.get_rect()                                   #Define rect as the size of road image



    def __init__(self):
        self.img = transform.scale(self.img, [1920, 180])   #Change size of road
        self.rect = self.img.get_rect()
