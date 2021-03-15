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
    img = image.load("assets\\road.png")
    rect = img.get_rect()

    def __init__(self):
        self.img = transform.scale(self.img, [1920, 180])
        self.rect = self.img.get_rect()
