from socket import *
import threading
from Network.thread import uploadThread
from Network.client import client

from classes.car import car
from classes.road import road
from pygame import TEXTINPUT, image, display, init, event, QUIT, transform

#Global variables
l = threading.Lock()

def simulation(Client):
    init()
    size = width, height = 1920, 1000
    display.set_caption("car: " + Client.clientNum.__str__())
    screen = display.set_mode(size)
    numOfRoads = 0
    numOfCars = 10
    cars = []
    Road = road()
    while ((Road.rect.y + Road.rect.height) <= 1000):
        screen.blit(Road.img, Road.rect)
        Road.rect.y += (Road.rect.height + 10)
        numOfRoads += 1
    for i in range(Client.clients):
        cars.append(car(numOfRoads, "assets\\car.png", screen, width, Road.rect.height, i))
    for i in range(numOfCars):
        cars.append(car(
            numOfRoads, "assets\\car2.png", screen, width, Road.rect.height, i))
    Car = cars[Client.clientNum]

    run = True

    while run and display.get_active():
        numOfRoads = 0
        Road.rect.y = 0
        global data

        for e in event.get():
            if e.type == QUIT:

                run = False
            if e.type == TEXTINPUT:
                txt = e.text
                Car.movement(txt)
        Client.data = Car.speed.__str__() + "," + Car.rect.center.__str__()
        l.acquire()
        if Client.locations.__len__() == cars.__len__():
            for i in range(cars.__len__()):
                location = Client.locations[i].split("(")
                if not i == Client.clientNum:
                    print(location)
                    cars[i].speed = float(location[0])
                    cars[i].rect.center = (int(location[1].strip(")").split(
                        ",")[0]), int(location[1].strip(")").split(",")[1]))
        l.release()
        print()

        screen.fill([0, 0, 0])
        # Move the car
        for c in cars:
            c.rect = c.rect.move(c.speed, 0)

        while ((Road.rect.y + Road.rect.height) <= 1000):                       # Render the road
            screen.blit(Road.img, Road.rect)
            Road.rect.y += (Road.rect.height + 10)
            numOfRoads += 1
        #bounds and collision
        for c in cars:
            c.outOfBounds(width, numOfRoads, Road.rect.height)
            screen.blit(c.img, c.rect)
            textrect = c.text.get_rect()
            textrect.center = c.rect.center
            textrect.top = c.rect.bottom
            screen.blit(c.text, textrect)
            if Car.rect.colliderect(c) and not Car == c:
                if Car.rect.x > c.rect.x:
                    c.movement(" ")
                    Car.rect.left = c.rect.right
                elif Car.rect.x < c.rect.x:
                    Car.movement(" ")
                    Car.rect.right = c.rect.left
        display.flip() 


def main():
    c = client()
    c.start()
    while True:
        if c.joined and c.started:
            simulation(c)
            c.stop()
            break
    print("main thread finished")


if __name__ == "__main__":
    main()
