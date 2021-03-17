from socket import AF_INET, SOCK_STREAM, socket
import socketserver
import sys
import threading
from Network.thread import uploadThread

from classes.car import car
from classes.road import road
from pygame import KEYDOWN, MOUSEBUTTONDOWN, TEXTINPUT, image, display, init, event, QUIT, transform, mouse, font

init()
size = width, height = 1920, 1000
screen = display.set_mode(size)
playerPos = []
simState = False
font = font.Font("freesansbold.ttf", 32)


class socketServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.HOST = ""
        self.PORT = 8888
        self.CONN_COUNTER = 0
        self.running_sockets = []
        self.s = socket(AF_INET, SOCK_STREAM)  # socket

    def run(self):
        self.s.bind((self.HOST, self.PORT))  # bind
        self.s.listen(1)  # listen
        while not simState:  # loop until game is executed
            c, a = self.s.accept()  # accept
            client = client_connection(c, a)
            self.running_sockets.append(client.start())  # fork
        print("Socket server finished")

    def stop(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(("127.0.0.1", self.PORT))
        s.send(bytes("quit", 'utf-8'))
        s.close()


class client_connection(threading.Thread):
    def __init__(self, client, addr):
        threading.Thread.__init__(self)
        self.BUFFER_SIZE = 1024
        self.c = client
        self.r = ""
        print(threading.Thread.getName(self) + " created.")

    def run(self):
        try:
            while True:
                self.r = self.c.recv(self.BUFFER_SIZE).decode("utf-8")
                if not self.r == "":
                    print(self.r)
                    print(threading.Thread.getName(self))
                if self.r == "quit":
                    print("Client on " + threading.Thread.getName(self) +
                          " ended the connection by keyword.")
                    return
        except:
            print("Client on " + threading.Thread.getName(self) +
                  " ended the connection by exception (close window).")
            return


def simulation():
    global simState
    simState = True
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

        for i in range(cars.__len__()):
            cars[i].outOfBounds(width, numOfRoads, Road.rect.height)
            screen.blit(cars[i].img, cars[i].rect)

        for i in range(cars.__len__()):
            for j in range(cars.__len__()):
                while cars[i].rect.colliderect(cars[j]) and not i == j:
                    cars[i].rect.x -= 1
                    cars[j].rect.x += 1
        display.flip()


def menu():
    global simState
    screen.fill((255, 255, 255))
    square = image.load("assets\\start_button.png")
    squarerect = square.get_rect()
    squarerect.center = screen.get_rect().center
    screen.blit(square, squarerect)
    numClients = font.render(
        "total clients: " + playerPos.__len__().__str__(), True, (0, 0, 0))
    numClientsRect = numClients.get_rect()
    numClientsRect.top = screen.get_rect().top
    numClientsRect.centerx = screen.get_rect().centerx
    screen.blit(numClients, numClientsRect)
    for e in event.get():
        if e.type == MOUSEBUTTONDOWN and squarerect.collidepoint(mouse.get_pos()):
            simState = True
        if e.type == QUIT:
            simState = True
    display.flip()


def main():
    s = socketServer()
    s.start()
    while not simState:
        menu()
    s.stop()
    simulation()
    print("Main thread finished.")


if __name__ == "__main__":
    main()
