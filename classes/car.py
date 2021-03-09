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
from pygame.constants import TEXTINPUT

class car:
    speed = 0
    img = image.load("assets\\car.png")
    rect = img.get_rect()
    img = transform.scale(img, [int(rect.width/4),int(rect.height/4)])
    rect = img.get_rect()

    def movement(self, e):
        if e.type == TEXTINPUT:
            txt = e.text

            if txt == "d":
                if self.speed < 7:
                    self.speed += 1

            if txt == "a":
                if self.speed > -3:
                    self.speed -= 1


            if txt == "s":
                if self.rect.y == 8:
                    self.rect.y = 142

            if txt == "w":
                if self.rect.y == 142:
                    self.rect.y = 8


