from Network.thread import uploadThread

from classes import car, road
from pygame import TEXTINPUT, image, display, init, event, QUIT, transform


init()
size = width, height = 1920, 1000
screen = display.set_mode(size)
numOfRoads = 0
numOfCars = 10


def main():
    global numOfRoads
    Car = car.car()
    AICars = []
    cars = []
    Road = road.road().create(Car.rect.height)
    while ((Road.rect.y + Road.rect.height) <= 1000):
        screen.blit(Road.img, Road.rect)
        Road.rect.y += (Road.rect.height + 10)
        numOfRoads += 1

    manualCar = Car.create(numOfRoads, "assets\\car.png", screen, width)
    cars.append(manualCar)
    for i in range(numOfCars):
        AICars.append(Car.create(
            numOfRoads, "assets\\car2.png", screen, width))
        cars.append(AICars[i])
    run = True
    while run and display.get_active():
        numOfRoads = 0
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == TEXTINPUT:
                if e.text == "u":
                    upload = uploadThread(data=[5, 5, 5, 5, 5])
                    upload.start()
            Car.movement(e)

        screen.fill([0, 0, 0])
        # Move the car
        Car.rect = Car.rect.move(Car.speed, 0)

        while ((Road.rect.y + Road.rect.height) <= 1000):                       # Render the road
            screen.blit(Road.img, Road.rect)
            Road.rect.y += (Road.rect.height + 10)
            numOfRoads += 1
        Car.outOfBounds(width, numOfRoads)

        for i in range(cars.__len__()):
            screen.blit(cars[i].img, cars[i].rect)

        Road.rect.y = 0

        # screen.blit(Car.img, Car.rect)                                          # Render the car

        display.flip()


if __name__ == "__main__":
    main()
