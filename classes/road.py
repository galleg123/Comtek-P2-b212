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
        self.rect = self.img.get_rect()
