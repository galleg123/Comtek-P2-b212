from socket import *
import threading
from time import time as t
from Network.client import Downlink, Uplink

from classes.car import car
from classes.road import road
from pygame import TEXTINPUT, image, display, init, event, QUIT, transform, font, time
#Global variables
l = threading.Lock()

#serverIP = "10.225.171.52" #thomas
#serverIP = "37.97.6.130" #kenneth
serverIP = "127.0.0.1" #localhost

serverPort = 8888

def simulation(DownLink: Downlink, UpLink: Uplink):
    init()

    FPS = 30
    fpsClock = time.Clock()

    f = font.Font("freesansbold.ttf", 32)
    size = width, height = 1500, 1000
    display.set_caption("car: " + str(DownLink.clientNum))
    screen = display.set_mode(size)
    numOfRoads = 0
    numOfCars = 30
    cars:list[car] = []
    Road = road()
    while ((Road.rect.y + Road.rect.height) <= 1000):
        screen.blit(Road.img, Road.rect)
        Road.rect.y += (Road.rect.height + 10)
        numOfRoads += 1
    for i in range(DownLink.clients):
        cars.append(car(numOfRoads, "assets\\car new.png", screen, width, Road.rect.height, i))
    for i in range(DownLink.clients,numOfCars):
        cars.append(car(
            numOfRoads, "assets\\car2 new.png", screen, width, Road.rect.height, i))
    Car = cars[DownLink.clientNum]

    #for speed testing
    cars[0].rect.x = 0
    cars[0].rect.y = 5 + (Road.rect.height + 10) * 0
    cars[0].movement("d")
    starttime = t()

    run = True
    frame_counter = 0
    fps_start = t()
    while run and display.get_active():
        numOfRoads = 0
        Road.rect.y = 0

        for e in event.get():
            if e.type == QUIT:

                run = False
            if e.type == TEXTINPUT:
                txt = e.text
                Car.movement(txt)
        UpLink.data = str(int(Car.speed)) + "," + str(Car.rect.center)
        l.acquire()
        if len(DownLink.locations) == len(cars):
            for i in range(len(cars)):
                location = DownLink.locations[i].split("(")
                if not i == DownLink.clientNum:
                    try:
                        speed = float(location[0])
                        center = (int(location[1].strip(")").split(",")[0]), int(location[1].strip(")").split(",")[1]))
                        cars[i].speed = speed
                        cars[i].rect.center = center
                    except:
                        print(location)
                    DownLink.newdata = False
        l.release()

        screen.fill([0, 0, 0])
        while ((Road.rect.y + Road.rect.height) <= 1000):                       # Render the road
            screen.blit(Road.img, Road.rect)
            Road.rect.y += (Road.rect.height + 10)
            numOfRoads += 1
        #bounds and collision
        for c in cars:
            #move the cars
            c.rect = c.rect.move(c.speed, 0)

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

        if cars[0].rounds > 0 and cars[0].roundb:
            cars[0].roundb = False
            time_end = t()
            print("{}. round trip time: {}".format(cars[0].rounds, (time_end-starttime)))
            starttime = t()
        
        frame_counter += 1
        fps_end = t()
        fps = int(frame_counter / float(fps_end - fps_start))
        fpstext = f.render("FPS: {}".format(fps), True, (255,255,255))
        fpstextrect = fpstext.get_rect()
        fpstextrect.top = screen.get_rect().top
        fpstextrect.right = screen.get_rect().right
        speedtext = f.render("Speed: {}".format(cars[DownLink.clientNum].speed), True, (255,255,255))
        speedtextrect = speedtext.get_rect()
        speedtextrect.top = fpstextrect.bottom
        speedtextrect.right = screen.get_rect().right
        screen.blit(fpstext, fpstextrect)
        screen.blit(speedtext, speedtextrect)

        Dtext = f.render("accelerate the car", True, (255,255,255))
        Dtextrect = Dtext.get_rect()
        Dtextrect.bottom = screen.get_rect().bottom
        Dtextrect.right = screen.get_rect().right
        D = image.load("assets\\keys\\D.png")
        Drect = D.get_rect()
        Drect.center = Dtextrect.center
        Drect.bottom = Dtextrect.top
        Spacetext = f.render("brake the car", True, (255,255,255))
        Spacetextrect = Spacetext.get_rect()
        Spacetextrect.center = Drect.center
        Spacetextrect.bottom = Drect.top
        Space = image.load("assets\\keys\\Space.png")
        Spacerect = Space.get_rect()
        Spacerect.center = Spacetextrect.center
        Spacerect.bottom = Spacetextrect.top
        screen.blit(Dtext,Dtextrect)
        screen.blit(D,Drect)
        screen.blit(Spacetext,Spacetextrect)
        screen.blit(Space,Spacerect)


        

        display.flip()
        fpsClock.tick(FPS)


def main():

    #new stuff
    joined = False
    while not joined:
        In = input("write join to join a session: ")
        if In == "join":
            s = socket(AF_INET,SOCK_STREAM)
            s.connect((serverIP, serverPort))
            s.send(bytes(In, "utf-8"))
            print("joined")
            joined = True
            Dlink = Downlink(s)
            Ulink = Uplink(s)
            Dlink.start()
            Ulink.start()

    #new stuff
    while True:
        if joined and Dlink.started:
            simulation(Dlink, Ulink)
            Dlink.stop()
            Ulink.stop()
            break
    print("main thread finished")


if __name__ == "__main__":
    main()
