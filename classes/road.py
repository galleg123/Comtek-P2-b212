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
    img = image.load("assets\\road new.png")                    #Load image of road
    rect = img.get_rect()                                   #Define rect as the size of road image



    def __init__(self):
        self.img = transform.scale(self.img, [int(self.rect.width*1.5), int(self.rect.height)])   #Change size of road
        self.rect = self.img.get_rect()
