import pygame
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
from pygame import constants
from pygame.constants import TEXTINPUT


class car:
    speed = 10
    acceleration = 0
    deceleration = 1.0
    breaklengt = (speed**2)/(2*deceleration)
    img = image.load("assets\\car.png")
    rect = img.get_rect()
    img = transform.scale(img, [int(rect.width/4), int(rect.height/4)])
    rect = img.get_rect()

    def movement(self, e):
        if e.type == TEXTINPUT:
            txt = e.text

            if txt == "d":
                if self.speed < 44:
                    self.acceleration = 0.2 # 99% på at det var en dårlig ide med self.acceleration += 0.5
                    self.speed =self.speed+(self.speed**self.acceleration) #Det skal være en logaritmisk aftagende funktion eller en form for diminishing returns
                if self.speed == 0:
                    self.speed = 2

            if txt == " ":
                if self.speed >= 0:
                    self.acceleration = 0.5
                    self.speed =self.speed-(self.speed**self.acceleration)
                    print(self.speed)
                if self.speed < 0:
                    self.speed = 0

            if txt == "s":
                if self.rect.y == 5:
                    self.rect.y = 100

            if txt == "w":
                if self.rect.y == 100:
                    self.rect.y = 5

    def outOfBounds(self, screenwidth, roads, roadheight):
        if (self.rect.x + (self.rect.width/2)) > screenwidth:
            if not self.rect.y == (((roadheight) + 10) * (roads-1)) + 5 and not self.rect.y >= (((roadheight) + 10) * (roads-1)) + 100:
                self.rect.y += (roadheight + 10)
                self.rect.x = 0 - (self.rect.width/2)
            else:
                self.rect.y = 5
                self.rect.x = 0 - (self.rect.width/2)

        if (self.rect.x + (self.rect.width/2)) < 0:
            if not self.rect.y <= 5 and not self.rect.y == 100:
                self.rect.y -= (roadheight + 10)
                self.rect.x = 1920 - (self.rect.width/2)
            else:
                self.rect.y += (roadheight) * (roads)
                self.rect.x = 1920 - (self.rect.width/2)

    def __init__(self, roads, Image, screen, width, roadheight):
        screen.blit(self.img, self.rect)
        self.img = image.load(Image)
        self.img = transform.scale(
            self.img, [int(self.rect.width), int(self.rect.height)])
        self.rect = self.img.get_rect()
        self.rect.x = random.randint(0, width)
        self.rect.y = 5 + (roadheight + 10) * random.randint(0, roads - 1)
