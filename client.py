from socket import *
import threading
from Network.thread import uploadThread

from classes.car import car
from classes.road import road
from pygame import TEXTINPUT, image, display, init, event, QUIT, transform

data = "placeholder"


class client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.SERVER_IP = "192.168.0.100"
        self.SERVER_PORT = 8888
        self.BUFFER_SIZE = 1024
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((self.SERVER_IP, self.SERVER_PORT))

    def run(self):
        global data
        self.joined = False
        while True:
            In = input("write join to join a session: ")
            if In.__len__() > 0:
                self.s.send(bytes(In, 'utf-8'))
                print("data sent.")
            if In == "join":
                self.joined = True
                break
            if In == "quit":
                self.s.close()
                return
        
        self.started = False
        while self.joined:
            print("listening...")
            r = self.s.recv(self.BUFFER_SIZE).decode('utf-8')
            print("received data: " + r)
            if r == "start":
                self.started = True
            print(data)
            if data.__len__() > 0:
                self.s.send(bytes(data, 'utf-8'))
                print("location sent.")
    def stop(self):
        self.s.close()
        self.joined = False

def simulation():
    init()
    size = width, height = 1920, 1000
    screen = display.set_mode(size)
    numOfRoads = 0
    numOfCars = 10
    cars = []
    Road = road()
    while ((Road.rect.y + Road.rect.height) <= 1000):
        screen.blit(Road.img, Road.rect)
        Road.rect.y += (Road.rect.height + 10)
        numOfRoads += 1

    Car = car(numOfRoads, "assets\\car.png", screen, width, Road.rect.height)
    cars.append(Car)
    for i in range(numOfCars):
        cars.append(car(
            numOfRoads, "assets\\car2.png", screen, width, Road.rect.height))

    run = True

    while run and display.get_active():
        numOfRoads = 0
        Road.rect.y = 0
        global data
        
        for e in event.get():
            if e.type == QUIT:
                
                run = False
            if e.type == TEXTINPUT:
                if e.text == "u":
                    upload = uploadThread(data=[int(cars[1].speed), int(
                        cars[2].speed), int(cars[3].speed), int(cars[4].speed), int(cars[5].speed)])
                    upload.start()
            Car.movement(e)
        data = Car.speed.__str__() + "," + Car.rect.center.__str__()

        screen.fill([0, 0, 0])
        # Move the car
        for i in range(cars.__len__()):
            cars[i].rect = cars[i].rect.move(cars[i].speed, 0)

        while ((Road.rect.y + Road.rect.height) <= 1000):                       # Render the road
            screen.blit(Road.img, Road.rect)
            Road.rect.y += (Road.rect.height + 10)
            numOfRoads += 1

        for i in range(cars.__len__()):
            cars[i].outOfBounds(width, numOfRoads, Road.rect.height)
            screen.blit(cars[i].img, cars[i].rect)

        
        for i in range(cars.__len__()):
            for j in range(cars.__len__()):
                while cars[i].rect.colliderect(cars[j]) and not i == j:
                    cars[i].rect.x -= 1
                    cars[j].rect.x += 1
        display.flip()

def main():
    c = client()
    c.start()
    while True:
        if c.joined and c.started:
            simulation()
            c.stop()
            break
    print("main thread finished")


if __name__ == "__main__":
    main()
