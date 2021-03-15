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
from pygame.constants import TEXTINPUT


class car:
    speed = 0
    acceleration = 0
    img = image.load("assets\\car.png")
    rect = img.get_rect()
    img = transform.scale(img, [int(rect.width/4), int(rect.height/4)])
    rect = img.get_rect()

    def movement(self, e):
        if e.type == TEXTINPUT:
            txt = e.text

            if txt == "d":
                if self.acceleration < 44:
                    self.acceleration += 0.5
                    self.speed = 1.08**self.acceleration

            if txt == " ":
                if self.acceleration >= -10:
                    self.acceleration -= 1
                    self.speed = 1.08**self.acceleration

            if txt == "s":
                if self.rect.y == 6:
                    self.rect.y = 107

            if txt == "w":
                if self.rect.y == 107:
                    self.rect.y = 6

    def outOfBounds(self, screenwidth, roads):
        if self.speed > 0:
            if (self.rect.x + (self.rect.width/2)) >= screenwidth:
                if not self.rect.y == (((self.rect.height*2.5) + 10) * (roads-2)) + 6 and not self.rect.y >= (((self.rect.height*2.5) + 10) * (roads-2)) + 107:
                    self.rect.y += (self.rect.height*2.5 + 10)
                    self.rect.x = 0 - (self.rect.width/2)
                else:
                    self.rect.y = 6
                    self.rect.x = 0 - (self.rect.width/2)

        if self.speed < 0:
            if (self.rect.x + (self.rect.width/2)) <= 0:
                if not self.rect.y <= 6 and not self.rect.y == 107:
                    self.rect.y -= (self.rect.height*2.5 + 10)
                    self.rect.x = 1920 - (self.rect.width/2)
                else:
                    self.rect.y += (self.rect.height*2.5 + 10) * (roads - 1)
                    self.rect.x = 1920 - (self.rect.width/2)

    def __init__(self, roads, Image, screen, width):
        screen.blit(self.img, self.rect)
        self.img = image.load(Image)
        self.img = transform.scale(
            self.img, [int(self.rect.width), int(self.rect.height)])
        self.rect = self.img.get_rect()
        self.rect.x = random.randint(0, width)
        self.rect.y = 6 + (self.rect.height * 2.5 + 10) * random.randint(0, roads)
