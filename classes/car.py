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
    gear = 0
    speed = 0
    img = image.load("assets\\car.png")
    rect = img.get_rect()
    img = transform.scale(img, [int(rect.width/3),int(rect.height/3)])
    rect = img.get_rect()

    def movement(self, e):
        if e.type == TEXTINPUT:
            txt = e.text
            if txt == "q":
                if self.gear > -2:
                    self.gear -= 1
            if txt == "e":
                if self.gear < 6:
                    self.gear += 1
            if txt == "w":
                self.speed = 1 * self.gear
            if txt == "s":
                if self.speed < 0:
                    self.gear += 1
                    self.speed += self.gear * 1
                if self.speed > 0:
                    self.gear -= 1
                    self.speed -= self.gear * 1
            if txt == "d":
                if self.rect.y == 8:
                    self.rect.y = 142

            if txt == "a":
                if self.rect.y == 142:
                    self.rect.y = 8


