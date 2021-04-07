import math
import pygame

speed = -0


for event in pygame.event.get():
    txt = event.text
    if txt == "d":
        if speed > 20:
            break
    speed = speed + 1

acceleration = 1.2**speed

print(speed)

