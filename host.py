from Database.database_Class import database
import random
from socket import AF_INET, SOCK_STREAM, socket
import socketserver
import sys
import threading
from time import time as t
from Network.thread import uploadThread
from Network.server import handler

from classes.car import car
from classes.road import road
from pygame import KEYDOWN, MOUSEBUTTONDOWN, TEXTINPUT, image, display, init, event, QUIT, transform, mouse, font, time


init()                                                                      
size = width, height = 1500, 1000                                           
screen = display.set_mode(size)
f = font.Font("freesansbold.ttf", 32)

FPS = 30
fpsClock = time.Clock()

l = threading.Lock()

def simulation(Handler):
    braking = False
    Handler.simState = True
    numOfRoads = 0
    numOfCars = 30
    counter = 0
    avgcounter = 0
    reactiontimer = False
    brakingcar = 0
    avground = 28.959772205352785
    starttime = t()

    cars = []
    Road = road()
    while Road.rect.y + Road.rect.height <= 1000:
        screen.blit(Road.img, Road.rect)
        Road.rect.y += (Road.rect.height + 10)
        numOfRoads += 1
    for i in range(Handler.clients.__len__()):
        Car = car(numOfRoads, "assets\\car new.png", screen, width, Road.rect.height, i)
        cars.append(Car)
    for i in range(Handler.clients.__len__(),numOfCars):
        cars.append(car(numOfRoads, "assets\\car2 new.png", screen, width, Road.rect.height, i))
    rl = []
    for c in cars:
        pt = image.load("assets\\point.png")
        ptrect = pt.get_rect()
        pt = transform.scale(pt, (ptrect.width*4, ptrect.height))
        ptrect = pt.get_rect() 
        ptrect.center = (c.rect.left - c.rect.width, c.rect.centery)
        rl.append(ptrect)
    fps_start = t()
    frame_counter = 0
    while display.get_active() and Handler.clients.__len__() > 0:
        numOfRoads = 0
        Road.rect.y = 0

        for e in event.get():
            if e.type == QUIT:
                return
            if e.type == TEXTINPUT:
                if e.text == "u":
                    for i in range(Handler.clients.__len__()):
                        db = database()
                        #db.start(data=[cars[i].average, ])#0 = average, 1 = time lost, 2 = reaction time

                if e.text == "b" and not braking:
                    print("braking")
                    rand = random.randint(Handler.clients.__len__(), cars.__len__()-1)
                    brakingcar = cars[rand]
                    braking = True
        Handler.data = "0:{}{}".format(int(cars[0].speed).__str__(), cars[0].rect.center.__str__())
        for i in range(cars.__len__() - 1):
            Handler.data += (";{}:{}{}".format((i + 1).__str__(), int(cars[i + 1].speed).__str__(), cars[i + 1].rect.center.__str__()))
        l.acquire()
        for i in range(Handler.locations.__len__()):
            if not Handler.locations.get(i) == "placeholder":
                location = Handler.locations.get(i).split(",")
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
                print("speed: {}".format(c.speed))
            c.outOfBounds(width, numOfRoads, Road.rect.height)
            screen.blit(c.img, c.rect)
            textrect = c.text.get_rect()
            textrect.center = c.rect.center
            textrect.top = c.rect.bottom
            screen.blit(c.text, textrect)
            rl[c.num].center = (c.rect.left - c.rect.width, c.rect.centery)
            screen.blit(pt,rl[c.num])
            for C in cars:
                while c.rect.colliderect(C) and not c == C and not c.num < Handler.clients.__len__():
                    if c.rect.left <= C.rect.left:
                        c.movement(" ")
                        c.rect.x -= 5
                        #C.rect.x += 5
                    elif c.rect.right > C.rect.right:
                        C.movement(" ")
                        #c.rect.x += 5
                        C.rect.x -= 5
            check = c.rect.collidelist(rl)
            if Handler.mode == 1 and c.speed < c.maxspeed and not check > -1 and not c == brakingcar:
                #print("accelerating car {}".format(c.num))
                #accelerate cars if there are none in front of it
                c.movement("d")
                if c.num <= Handler.clients.__len__():
                    pass
                if c.num <= Handler.clients.__len__() and c.speed < 1:
                    c.time = 0
            elif Handler.mode == 0 and check > -1 and c.speed < cars[check].speed:
                c.movement("d")
                
        if braking:
            brakingcar.movement(" ")
            counter += 1
            if counter == 150:
                braking = False
                brakingcar = 0
                counter = 0

        #measurements
        #average
        avgcounter += 1
        if avgcounter == 500:
            avgcounter = 0
            for c in cars:
                c.speeds.append(c.speed)
                c.average = sum(c.speeds) / c.speeds.__len__()

        #time lost
        if cars[0].rounds > 0 and cars[0].timelostd:
            cars[0].timelostd = False
            lost_time = t() - starttime - avground
            print("time lost: {}".format(lost_time))
            starttime = t()

        if reactiontimer:
            pass
        
        #UI
        frame_counter += 1
        fps_end = t()
        fps = int(frame_counter / float(fps_end - fps_start))
        fpstext = f.render("FPS: {}".format(fps), True, (0,0,0))
        fpstextrect = fpstext.get_rect()
        fpstextrect.top = screen.get_rect().top
        fpstextrect.right = screen.get_rect().right
        screen.blit(fpstext, fpstextrect)

        Btext = f.render("brake a car",True,(255,255,255))
        Btextrect = Btext.get_rect()
        Btextrect.bottom = screen.get_rect().bottom
        Btextrect.right = screen.get_rect().right
        B = image.load("assets\\keys\\B.png")
        Brect = B.get_rect()
        Brect.center = Btextrect.center
        Brect.bottom = Btextrect.top
        Utext = f.render("upload data", True, (255,255,255))
        Utextrect = Utext.get_rect()
        Utextrect.center = Brect.center
        Utextrect.bottom = Brect.top
        U = image.load("assets\\keys\\U.png")
        Urect = U.get_rect()
        Urect.center = Utextrect.center
        Urect.bottom = Utextrect.top
        screen.blit(Btext,Btextrect)
        screen.blit(B,Brect)
        screen.blit(Utext, Utextrect)
        screen.blit(U, Urect)

        

        display.flip()
        fpsClock.tick(FPS)  



def menu(Handler):
    screen.fill((255, 255, 255))
    start = image.load("assets\\start_button.png")
    start = transform.scale(start,(int(start.get_width()/2),int(start.get_height()/2)))
    cacc = image.load("assets\\Cacc_simulation.png")
    cacc = transform.scale(cacc,(int(cacc.get_width()/2),int(cacc.get_height()/2)))
    manual = image.load("assets\\manual_simulation.png")
    manual = transform.scale(manual,(int(manual.get_width()/2),int(manual.get_height()/2)))
    startrect = start.get_rect()
    caccrect = cacc.get_rect()
    manualrect = manual.get_rect()
    startrect.center = screen.get_rect().center
    caccrect.center = (screen.get_rect().centerx/2,screen.get_rect().centery/2)
    manualrect.center = (screen.get_rect().centerx + screen.get_rect().centerx/2, screen.get_rect().centery/2)
    screen.blit(start, startrect)
    screen.blit(cacc,caccrect)
    screen.blit(manual,manualrect)
    numClients = f.render(
        "total clients: " + Handler.clients.__len__().__str__(), True, (0, 0, 0))
    numClientsRect = numClients.get_rect()
    numClientsRect.top = screen.get_rect().top
    numClientsRect.centerx = screen.get_rect().centerx
    screen.blit(numClients, numClientsRect)
    for e in event.get():
        if e.type == MOUSEBUTTONDOWN:
            if startrect.collidepoint(mouse.get_pos()):
                Handler.simState = True
            if caccrect.collidepoint(mouse.get_pos()):
                Handler.mode = 0
                pass
            if manualrect.collidepoint(mouse.get_pos()):
                Handler.mode = 1
                pass
        if e.type == QUIT:
            Handler.simState = True
    display.flip()





def main():
    h = handler()
    h.start()
    while not h.simState:
        menu(h)
    h.stop()
    simulation(h)
    print("simulation finished")
    for c in h.clients:
        print("closing client {}".format(c.getName()))
        c.close()
    print("Main thread finished.")


if __name__ == "__main__":
    main()
