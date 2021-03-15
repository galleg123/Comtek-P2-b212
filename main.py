from Network.thread import uploadThread

from classes.car import car
from classes.road import road
from pygame import TEXTINPUT, image, display, init, event, QUIT, transform


init()
size = width, height = 1920, 1000
screen = display.set_mode(size)
numOfRoads = 0
numOfCars = 10


def main():
    global numOfRoads
    AICars = []
    cars = []
    Road = road()
    while ((Road.rect.y + Road.rect.height) <= 1000):
        screen.blit(Road.img, Road.rect)
        Road.rect.y += (Road.rect.height + 10)
        numOfRoads += 1

    Car = car(numOfRoads, "assets\\car.png", screen, width, Road.rect.height)
    cars.append(Car)
    for i in range(numOfCars):
        AICars.append(car(
            numOfRoads, "assets\\car2.png", screen, width, Road.rect.height))
        cars.append(AICars[i])

    run = True

    while run and display.get_active():
        numOfRoads = 0
        for e in event.get():
            if e.type == QUIT:
                run = False
            if e.type == TEXTINPUT:
                if e.text == "u":
                    upload = uploadThread(data=[int(cars[1].speed), int(
                        cars[2].speed), int(cars[3].speed), int(cars[4].speed), int(cars[5].speed)])
                    upload.start()
            Car.movement(e)

        screen.fill([0, 0, 0])
        # Move the car
        for i in range(cars.__len__()):
            cars[i].rect = cars[i].rect.move(cars[i].speed, 0)

        while ((Road.rect.y + Road.rect.height) <= 1000):                       # Render the road
            screen.blit(Road.img, Road.rect)
            Road.rect.y += (Road.rect.height + 10)
            numOfRoads += 1
        #Car.outOfBounds(width, numOfRoads)

        for i in range(cars.__len__()):
            cars[i].outOfBounds(width, numOfRoads, Road.rect.height)
            screen.blit(cars[i].img, cars[i].rect)

        Road.rect.y = 0
        for i in range(cars.__len__()):
            for j in range(cars.__len__()):
                while cars[i].rect.colliderect(cars[j]) and not i == j:
                    cars[i].rect.x -= 1
                    cars[j].rect.x += 1
        # screen.blit(Car.img, Car.rect)                                          # Render the car

        display.flip()


if __name__ == "__main__":
    main()
