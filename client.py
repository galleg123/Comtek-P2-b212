from socket import *
import threading
from Network.thread import uploadThread

from classes.car import car
from classes.road import road
from pygame import TEXTINPUT, image, display, init, event, QUIT, transform

#Global variables
data = "placeholder"                                                        
locations = {}                                                              
clientNum = 0                                                               
clients = 0

l = threading.Lock()

# seperate thread to keep the connection to the server going while the simulation is running
class client(threading.Thread):                                             
    def __init__(self):                                                     
        threading.Thread.__init__(self)                                     
        self.SERVER_IP = "10.225.171.52"                                    
        #self.SERVER_IP = "62.107.59.124"
        self.SERVER_PORT = 8888                                             
        self.BUFFER_SIZE = 1024                                             
        self.s = socket(AF_INET, SOCK_STREAM)                               
        self.s.connect((self.SERVER_IP, self.SERVER_PORT))                  

#Method that is run when the thread is started
    def run(self):                                                          
        global data                                                         
        global locations                                                    
        global clientNum                                                    
        global clients
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
            r = self.s.recv(self.BUFFER_SIZE).decode('utf-8')               
            if not r == "placeholderplaceholder" and not r.split(",")[0] == "start":    
                #print(r)
                dataArray = r.split(";")                                    
                for d in dataArray:                                         
                    locations[int(d.split(":")[0])] = d.split(":")[1]       
            if r.split(",")[0] == "start":                                  
                clientNum = int(r.split(",")[1]) -1                         
                clients = int(r.split(",")[2])
                self.started = True                                         
            if data.__len__() > 0:                                          
                self.s.send(bytes(data, 'utf-8'))                           

    #method that is called to close the connection and stop the program, used to avoid exceptions
    def stop(self):                     
        self.s.close()                  
        self.joined = False             



def simulation():
    global clientNum
    init()
    size = width, height = 1920, 1000
    display.set_caption("car: " + clientNum.__str__())
    screen = display.set_mode(size)
    numOfRoads = 0
    numOfCars = 10
    cars = []
    Road = road()
    while ((Road.rect.y + Road.rect.height) <= 1000):
        screen.blit(Road.img, Road.rect)
        Road.rect.y += (Road.rect.height + 10)
        numOfRoads += 1
    for i in range(clients):
        cars.append(car(numOfRoads, "assets\\car.png", screen, width, Road.rect.height, i))
    for i in range(numOfCars):
        cars.append(car(
            numOfRoads, "assets\\car2.png", screen, width, Road.rect.height, i))
    Car = cars[clientNum]

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
        l.acquire()
        if locations.__len__() == cars.__len__():
            for i in range(cars.__len__()):
                location = locations[i].split("(")
                if not i == clientNum:
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
                    c.speed = Car.speed
                    Car.rect.left = c.rect.right
                elif Car.rect.x < c.rect.x:
                    Car.speed = c.speed
                    Car.rect.right = c.rect.left
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
