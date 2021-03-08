import random
import sys
from pygame import (
    image,
    display,
    init,
    event,
    QUIT,
    transform,
)

class car:
    speed = 0
    img = image.load("assets\\car.png")
    rect = img.get_rect()
    img = transform.scale(img, [int(rect.width/3),int(rect.height/3)])
    rect = img.get_rect()