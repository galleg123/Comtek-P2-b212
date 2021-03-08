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
    img = image.load("assets\\car.png")
    rect = img.get_rect()
    img = transform.scale(img, [int(rect.x/2),int(rect.y/2)])
    rect = img.get_rect()