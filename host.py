from socket import AF_INET, SOCK_STREAM, socket
import socketserver
import sys
import threading
from Network.thread import uploadThread
from Network.socketServer import socketServer

from classes.car import car
from classes.road import road
from pygame import KEYDOWN, MOUSEBUTTONDOWN, TEXTINPUT, image, display, init, event, QUIT, transform, mouse, font

init()                                                                      
size = width, height = 1920, 1000                                           
screen = display.set_mode(size)                                          
font = font.Font("freesansbold.ttf", 32)                                    
                                                          

l = threading.Lock()

def simulation(Host):
    Host.simState = True
    numOfRoads = 0
    numOfCars = 10

    cars = []
    Road = road()
    while Road.rect.y + Road.rect.height <= 1000:
        screen.blit(Road.img, Road.rect)
        Road.rect.y += (Road.rect.height + 10)
        numOfRoads += 1
    for i in range(Host.clients.__len__()):
        Car = car(numOfRoads, "assets\\car.png", screen, width, Road.rect.height, i)
        cars.append(Car)
    for i in range(Host.clients.__len__(),numOfCars+Host.clients.__len__()):
        cars.append(car(
            numOfRoads, "assets\\car2.png", screen, width, Road.rect.height, i))
    rl = []
    for c in cars:
        pt = image.load("assets\\point.png")
        ptrect = pt.get_rect()
        ptrect.center = (c.rect.left - c.rect.width, c.rect.centery)
        rl.append(ptrect)
    while display.get_active() and Host.clients.__len__() > 0:
        numOfRoads = 0
        Road.rect.y = 0

        for e in event.get():
            if e.type == QUIT:
                sys.exit()
            if e.type == TEXTINPUT:
                if e.text == "u":
                    upload = uploadThread(data=[int(cars[1].speed), int(
                        cars[2].speed), int(cars[3].speed), int(cars[4].speed), int(cars[5].speed)])
                    upload.start()
        #TODO: add header to trigger jam 
        Host.data = "0:{}{}".format(cars[0].speed.__str__(), cars[0].rect.center.__str__())
        for i in range(cars.__len__() - 1):
            Host.data += (";{}:{}{}".format((i + 1).__str__(), cars[i + 1].speed.__str__(), cars[i + 1].rect.center.__str__()))
        print(Host.locations)
        l.acquire()
        for i in range(Host.locations.__len__()):
            if not Host.locations.get(i) == "placeholder":
                location = Host.locations.get(i).split(",")
                cars[i].speed = float(location[0])
                cars[i].rect.center = (
                    int(location[1].strip("(")), int(location[2].strip(")")))
        l.release()
        screen.fill([0, 0, 0])
        while ((Road.rect.y + Road.rect.height) <= 1000):                       # Render the road
            screen.blit(Road.img, Road.rect)
            Road.rect.y += (Road.rect.height + 10)
            numOfRoads += 1
        #bounds and collision
        for c in cars:
            try:
                c.rect = c.rect.move(c.speed, 0)
            except:
                print(c.speed)
            c.outOfBounds(width, numOfRoads, Road.rect.height)
            screen.blit(c.img, c.rect)
            textrect = c.text.get_rect()
            textrect.center = c.rect.center
            textrect.top = c.rect.bottom
            screen.blit(c.text, textrect)
            rl[c.num].center = (c.rect.left - c.rect.width, c.rect.centery)
            screen.blit(pt,rl[c.num])
            for C in cars:
                while c.rect.colliderect(C) and not c == C and not c.num < Host.clients.__len__():
                    if c.rect.left <= C.rect.left:
                        c.movement(" ")
                        c.rect.x -= 5
                        #C.rect.x += 5
                    elif c.rect.right > C.rect.right:
                        C.movement(" ")
                        #c.rect.x += 5
                        C.rect.x -= 5
            check = c.rect.collidelist(rl)
            if c.speed < c.maxspeed and not check > -1:
                print("accelerating car {}".format(c.num))
                #accelerate cars if there are none in front of it
                c.movement("d")
        
        display.flip()


def menu(Host):
    screen.fill((255, 255, 255))
    square = image.load("assets\\start_button.png")
    squarerect = square.get_rect()
    squarerect.center = screen.get_rect().center
    screen.blit(square, squarerect)
    numClients = font.render(
        "total clients: " + Host.clients.__len__().__str__(), True, (0, 0, 0))
    numClientsRect = numClients.get_rect()
    numClientsRect.top = screen.get_rect().top
    numClientsRect.centerx = screen.get_rect().centerx
    screen.blit(numClients, numClientsRect)
    for e in event.get():
        if e.type == MOUSEBUTTONDOWN and squarerect.collidepoint(mouse.get_pos()):
            Host.simState = True
        if e.type == QUIT:
            Host.simState = True
    display.flip()


def main():
    s = socketServer()
    s.start()
    while not s.simState:
        menu(s)
    s.stop()
    simulation(s)
    for c in s.clients:
        c.close()
    print("Main thread finished.")


if __name__ == "__main__":
    main()
