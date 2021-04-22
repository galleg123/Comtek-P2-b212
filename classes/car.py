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
    font
)
from pygame import constants
from pygame.constants import TEXTINPUT
import math
import time


class car:
    speed = 10                                              
    speeds = []
    average = 0
    rounds = 0
    roundb = False
    acceleration = 0
    deceleration = 1.0
    breaklengt = (speed**2)/(2*deceleration)                                #Standard estimation for breaklength
    taskTime = 0
    accTime = 1
    maxspeed = 80/7.27                                                      #Max speed for the car, is set random between 2 values
    minAcceleration = 0.1                                                   #Minimum speed increase when accelerating
    img = image.load("assets\\car new.png")                                     #Load image of player controlled car
    rect = img.get_rect()                                                   #Define rect as the size of car image
    img = transform.scale(img, [int(rect.width), int(rect.height)])     #Change the size of car Size is equal to 4m long, and 2,4m wide
    rect = img.get_rect()

    def movement(self, txt):                                                  #Define movement for player controlled car
            if txt == "d":                                                  #If d is pressed
                #if self.speed < 1:                                          #If speed under 1, and d is pressed, change the speed to 1 so that the code below will work
                #    self.speed = 1
                #if self.speed < self.maxspeed:                              #If speed is under 44, and d is pressed gain speed with a given acceleration
                #    acceleration = 0.2 
                #    self.speed =self.speed+((self.speed**acceleration) + self.minAcceleration - 1)
                #if self.accTime >= 1:
                #    self.accTime = math.e**((0.02828854314*self.speed)-0.1216408355)
                if  int(round(time.time()*1000)) - self.taskTime > 1000:

                    if self.accTime <= 1:
                        self.accTime = 1


                    if self.speed < self.maxspeed:
                        self.accTime += 1
                        print(self.accTime)
                        print(self.speed)
                        self.speed = (4.3 + 35.35 * math.log(self.accTime))/7.27
                        self.taskTime = int(round(time.time()*1000))



            if txt == " ":                                                  #Brake function, when "space" is pressed
                #if self.speed > 0:                                          # If the speed is over 0 change the acceleration and use it to brake
                #    acceleration = 0.5
                #    self.speed =self.speed-(self.speed**acceleration)
                if  int(round(time.time()*1000)) - self.taskTime > 1000:

                    if self.speed < 0:                                          # If speed goes below 0, change it back to 0 so it doesn't drive backwards
                        self.speed = 0

                    if self.speed >= 0:
                        if self.accTime > 5:
                            self.accTime -= 3
                        if self.accTime > 0.89 and self.accTime <= 5:
                            self.accTime -= 1
                        
                        print(self.accTime)
                        print(self.speed)
                        if self.accTime < 0.89:
                            self.accTime = 0.89
                            
                        self.speed = (4.3 + 35.35 * math.log(self.accTime))/7.27
                        self.taskTime = int(round(time.time()*1000))


    def outOfBounds(self, screenwidth, roads, roadheight):                                          # Function that switches road if the car goes outside the screen
        if (self.rect.x + (self.rect.width/2)) > screenwidth:
            if not self.rect.y == (((roadheight) + 10) * (roads-1)) + 5 and not self.rect.y >= (((roadheight) + 10) * (roads-1)) + 100:             #Check what y position the car has to know which road it is on
                self.rect.y += (roadheight + 10)                                                     #If the road it is on, isn't the last road, then move down one road
                self.rect.x = 0 - (self.rect.width/2)                                                #Change the x position of the car so that it starts from the left on its new road position                   
            else:
                self.rect.y = 5                                                                      #If it is the last road it is on, change the y position to 5 so that is starts on the first road
                self.rect.x = 0 - (self.rect.width/2)                                                #Still the same x position change as above
                self.rounds += 1
                self.roundb = True

        if (self.rect.x + (self.rect.width/2)) < 0:                     # This function does the same as the above function, except in the other end of the road.
            if not self.rect.y <= 5 and not self.rect.y == 100:         # 
                self.rect.y -= (roadheight + 10)                        #
                self.rect.x = 1920 - (self.rect.width/2)                #
            else:
                self.rect.y += (roadheight) * (roads)                   #
                self.rect.x = 1920 - (self.rect.width/2)                # down to here is the same as the above, except for the other end of the road

    def __init__(self, roads, Image, screen, width, roadheight, num):        # Create an init that can be used to create more cars, as used for creating ai cars and player controlled cars
        screen.blit(self.img, self.rect)                                # Load in the car
        self.img = image.load(Image)                                    # Give the car an image
        self.img = transform.scale(
            self.img, [int(self.rect.width), int(self.rect.height)])    #Change the car to correct size
        self.rect = self.img.get_rect()     
        self.rect.x = random.randint(0, width)                          # Spawn the car at a random x position 
        self.rect.y = 5 + (roadheight + 10) * random.randint(0, roads - 1)  # Spawn the car at a random road
        self.maxspeed = random.randint(20,20)                              # Speed between 98, and  130
        self.text = font.Font("freesansbold.ttf", 32).render("{}. car".format(num), True, (0,0,0))
        self.num = num
