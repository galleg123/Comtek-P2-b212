from Network.server import handler
from Database.database_Class import database, find_max_value_test_id
from classes.car import car
from classes.road import road
import random
import threading
from time import time as t
from time import sleep

from pygame import KEYDOWN, MOUSEBUTTONDOWN, Rect, TEXTINPUT, image, display, init, event, QUIT, transform, mouse, font, time


init()
size = width, height = 1500, 1000
screen = display.set_mode(size)
f = font.Font("freesansbold.ttf", 32)

FPS = 30
fpsClock = time.Clock()

l = threading.Lock()

#testID = find_max_value_test_id()

def simulation(Handler: handler):
    braking = False
    Handler.simState = True
    numOfRoads = 0
    numOfCars = 30
    counter = 0
    avgcounter = 0
    brakingcar = 0
    brake = False
    running = True
    avground = 28.959772205352785
    starttime = t()
    cars:list[car] = []
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
    rl:list[Rect] = []
    for c in cars:
        pt = image.load("assets\\point.png")
        ptrect = pt.get_rect()
        pt = transform.scale(pt, (ptrect.width*4, ptrect.height))
        ptrect = pt.get_rect() 
        ptrect.center = (c.rect.left - c.rect.width, c.rect.centery)
        rl.append(ptrect) 
    fps_start = t()
    frame_counter = 0
    while display.get_active() and len(Handler.clients) > 0 and running == True:
        numOfRoads = 0
        Road.rect.y = 0
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == TEXTINPUT:

                if e.text == "b" and not braking:
                    print("braking")
                    rand = random.randint(len(Handler.clients), len(cars) - 1)
                    brakingcar = cars[rand]
                    braking = True
                if e.text == "t":
                    print("delay: {}".format(t() - delayTimer))
        delayTimer = t()
        Handler.data = "0:{}{}".format(str(int(cars[0].speed)), str(cars[0].rect.center))
        for i in range(len(cars) - 1):
            Handler.data += (";{}:{}{}".format((i + 1), int(cars[i + 1].speed), cars[i + 1].rect.center))
        l.acquire()
        for i in range(len(Handler.locations)):
            if not "placeholder" in Handler.locations:
                try:
                    location = Handler.locations.get(i).split(",")
                    speed = float(location[0])
                    center = (int(location[1].strip("(")), int(location[2].strip(")")))
                    cars[i].speed = speed
                    cars[i].rect.center = center
                except:
                    print(Handler.locations.get(i))
                #if Handler.newdata:
                Handler.newdata = False
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
                while c.rect.colliderect(C) and not c == C and not c.num < len(Handler.clients):
                    if c.rect.left <= C.rect.left:
                        c.movement(" ")
                        c.rect.x -= 5
                        #C.rect.x += 5
                    elif c.rect.right > C.rect.right:
                        C.movement(" ")
                        #c.rect.x += 5
                        C.rect.x -= 5
            check = c.rect.collidelist(rl)
            # slow cars if collision
            if check > -1:
                c.speed = cars[check].speed
                c.movement(" ")
                c.lowestDistance = cars[check].rect.left - c.rect.right 

            # for manual mode
            if Handler.mode == 1 and c.speed <= c.maxspeed and not check > 0 and not c == brakingcar:
                #accelerate cars if there are none in front of it
                c.movement("d")
                if c.num <= len(Handler.clients) and c.speed < 1:
                    c.time = 0

            # for cacc mode
            elif Handler.mode == 0 and check < 0 and c.speed < cars[check].speed:
                c.movement("d")

                #reaction time
            elif check > -1 and c.num <= len(Handler.clients) and c.reaction == False:
                print("reactiontimer started")
                c.reactiontimer = t()
                c.reaction = True
                c.startspeed = c.speed
            if c.reaction == True and c.startspeed > c.speed and not c.speed == 0:
                c.reactiontime = t() - c.reactiontimer
                c.reaction = False
                print("reaction time: {}".format(c.reactiontime))
            
            if c.speed > c.maxspeed:
                print("car {} has exceeded max speed".format(c.num))
        if braking:
            brakingcar.movement(" ")
            counter += 1
            if counter == 150:
                braking = False
                brakingcar = 0
                counter = 0
                brake = False
            elif brakingcar.speed <= 0 and not brake:
                print("brake successful")
                print(t()- starttime)
                brake = True

        #measurements
        #average
        avgcounter += 1
        if avgcounter == 500:
            avgcounter = 0
            for c in cars:
                c.speeds.append(c.speed)
                c.average = sum(c.speeds) / len(c.speeds)

        #time lost
        for i in range(len(Handler.clients)):
            if cars[i].rounds > 0 and cars[i].timelostd:
                cars[i].timelostd = False
                cars[i].lost_time = t() - starttime - avground
                print("time lost: {}".format(cars[i].lost_time))
                starttime = t()
        #UI
        frame_counter += 1
        fps_end = t()
        fps = int(frame_counter / float(fps_end - fps_start))
        fpstext = f.render("FPS: {}".format(fps), True, (255,255,255))
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
        if fps > 15:
            fpsClock.tick(FPS)  

    #upload to database
    #for i in range(len(Handler.clients)):
    #    db = database(testID, data=[cars[i].average, cars[i].lost_time, cars[i].reactiontime])
    #    db.start() #0 = average, 1 = time lost, 2 = reaction time
    #    sleep(0.5)

    #lowest distance test
    if len(Handler.clients) > 0:
        print("distance required: {}".format(Car.rect.width))
        for c in cars:
            print("car {} lowest distance: {}".format(c.num, c.lowestDistance))


def menu(Handler: handler):
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
    numClients = f.render("total clients: " + Handler.clients.__len__().__str__(), True, (0, 0, 0))
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
                print(Handler.mode)
                pass
            if manualrect.collidepoint(mouse.get_pos()):
                Handler.mode = 1
                print(Handler.mode)
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
    h.simState = False
    print("simulation finished")
    for c in h.clients:
        print("closing client {}".format(c.getName()))
        c.close()
    print("Main thread finished.")


if __name__ == "__main__":
    main()
