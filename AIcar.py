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

class AIcar:
    AIspeed = 0
    AIacceleration = 0
    AIimg = image.load("assets\\car2.png")
    AIrect = img.get_rect()
    AIimg = transform.scale(img, [int(rect.width/4),int(rect.height/4)])
    AIrect = img.get_rect()

    def movement(self, e):
        if e.type == TEXTINPUT:
            txt = e.text
   
            if self.AIacceleration < 44:
                self.AIacceleration += 0.5
                self.AIspeed = 1.08**self.AIacceleration
            
    def outOfBounds(self, screenwidth, roads):
        if self.AIspeed > 0:
            if (self.AIrect.x + (self.AIrect.width/2)) >= screenwidth:
                if not self.AIrect.y == (((self.AIrect.AIheight*2.5) + 10) * (roads-2)) + 6 and not self.AIrect.y >= (((self.AIrect.height*2.5) + 10) * (roads-2)) + 107:
                    self.AIrect.y += (self.AIrect.height*2.5 + 10)
                    self.AIrect.x = 0 - (self.AIrect.width/2)
                else:
                    self.AIrect.y = 6
                    self.AIrect.x = 0 - (self.AIrect.width/2)
        
        if self.AIspeed < 0:
            if (self.AIrect.x + (self.AIrect.width/2)) <= 0:
                if not self.AIrect.y <= 6 and not self.AIrect.y == 107:
                    self.AIrect.y -= (self.AIrect.height*2.5 + 10)
                    self.AIrect.x = 1920 - (self.AIrect.width/2)
                else:
                    self.AIrect.y += (self.AIrect.height*2.5 + 10) * (roads - 1)
                    self.AIrect.x = 1920 - (self.AIrect.width/2)
