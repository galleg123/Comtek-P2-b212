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
                if self.speed < 40:
                    self.speed += 1

            if txt == "a":
                if self.speed > -5:
                    self.speed -= 1


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
                if not self.rect.y == 6 and not self.rect.y <= 107:
                    self.rect.y -= (self.rect.height*2.5 + 10)
                    self.rect.x = 0 + (self.rect.width/2)
                else:
                    self.rect.y += (self.rect.height*2.5 + 10) * (roads - 1)
                    self.rect.x = 1920 + (self.rect.width/2)
            
        
