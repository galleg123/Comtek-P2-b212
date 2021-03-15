import sys
from classes.road import road
from classes.car import car
import threading

from pygame import QUIT, init, display, event


init()
size = width, height = 1920, 1000
screen = display.set_mode(size)
numRoads = 0
numCars = 10
AICars = []
cars = []
Road = road().create(car.rect.height)
while((Road.rect.y + Road.rect.height) <= 1000):
    screen.blit(Road.img, Road.rect)
    Road.rect.y += Road.rect.height + 10
    numRoads += 1
manualCar = car().create(numRoads, "assets\\car.png", screen, width)
cars.append(manualCar)
for i in range(numCars):
    AICars.append(car().create(numRoads, "assets\\car2.png", screen, width))
    cars.append(AICars[i])


class updateThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        print("running update")
        numRoads = 0
        for e in event.get():
            if e.type == QUIT:
                sys.exit()
        while Road.rect.y + Road.rect.height <= 1000:
            screen.blit(Road.img, Road.rect)
            Road.rect.y += Road.rect.height + 10
            numRoads += 1
        for i in range(cars.__len__()):
            screen.blit(cars[i].img, cars[i].rect)
        Road.rect.y = 0
        display.flip()


class mainThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        while display.get_active():
            print("running main")
            for e in event.get():
                if e.type == QUIT:
                    sys.exit()
                manualCar.movement(e)

            screen.fill([0, 0, 0])
            manualCar.rect = manualCar.rect.move(manualCar.speed, 0)
            uThread = updateThread(2)
            uThread.start()
        pass


class dataThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        pass


def main():
    mThread = mainThread(1)
    #dThread = dataThread(3)

    mThread.start()
    # dThread.start()
    print("main thread executed")


if __name__ == "__main__":
    main()
