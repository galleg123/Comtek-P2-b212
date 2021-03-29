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
clients = []                                                                
simState = False                                                            
font = font.Font("freesansbold.ttf", 32)                                    

data = "placeholder"                                                        
locations = {}                                                              

#The following class handles incoming sockets and seperates these into their own threads
class socketServer(threading.Thread):                                       
    def __init__(self):                                                     
        threading.Thread.__init__(self)                                     
        self.HOST = ""                                                      
        self.PORT = 8888                                                    
        self.CONN_COUNTER = 0                                               
        self.running_sockets = []                                           
        self.s = socket(AF_INET, SOCK_STREAM)                               

#this method is run whenever the start method is called and a thread is created
    def run(self):                                                          
        self.s.bind((self.HOST, self.PORT))                                 
        self.s.listen(1)                                                    
        while not simState:                                                 
            c, a = self.s.accept()                                          
            self.CONN_COUNTER += 1                                          
            client = client_connection(c, a, self.CONN_COUNTER)             
            self.running_sockets.append(client.start())                     
        print("Socket server finished")                                     

#this method is used to stop the socket server to avoid exceptions, this method simply lets the above code continue from accept
    def stop(self):                                                         
        s = socket(AF_INET, SOCK_STREAM)                                    
        s.connect(("127.0.0.1", self.PORT))                                 
        s.send(bytes("quit", 'utf-8'))                                      
        s.close()                                                           

#this class is used whenever a client is connecting to the host, it handles the client
class client_connection(threading.Thread):                                  
    def __init__(self, client, addr, num):                                  
        threading.Thread.__init__(self)                                     
        self.BUFFER_SIZE = 1024                                             
        self.c = client                                                     
        self.r = ""                                                         
        self.addr = addr                                                    
        self.num = num                                                      
        print(threading.Thread.getName(self) + " created.")                 

#this method is run whenever the start method is used
    def run(self):                                                          
        global data                                                         
        global locations                                                    
        try:                                                                
            while True:                                                     
                self.r = self.c.recv(self.BUFFER_SIZE).decode("utf-8")      
                if self.addr[0] == "127.0.0.1":                             
                    return                                                  
                elif not self.r == "":                                      
                    print(self.r)                                           
                    if self.r == "join":                                    
                        clients.append(self)                                 
                        break                                               
                elif self.r == "quit":                                      
                    print("Client on " + threading.Thread.getName(self) +   
                          " ended the connection by keyword.")
                    return                                                  
            started = False                                                 
            while True:                                                     
                if simState:                                                
                    if not started:                                         
                        self.c.send(
                            bytes("start," + self.num.__str__() + "," + clients.__len__().__str__(), 'utf-8'))  
                        print("start")                                      
                        started = True                                      
                    self.c.send(bytes(data, 'utf-8'))                       
                    self.data = self.c.recv(self.BUFFER_SIZE).decode('utf-8')   
                    locations[self.num-1] = self.data                       

        except:                                                             
            print("Client on " + threading.Thread.getName(self) +
                  " ended the connection by exception (close window).")     
            return                                                          

#method to stop the client connection, this is to avoid exceptions
    def close(self):                                                        
        self.c.close()                                                      
        print("closed client connection")                                   


def simulation():
    global simState
    global data
    simState = True
    numOfRoads = 0
    numOfCars = 10

    cars = []
    Road = road()
    while ((Road.rect.y + Road.rect.height) <= 1000):
        screen.blit(Road.img, Road.rect)
        Road.rect.y += (Road.rect.height + 10)
        numOfRoads += 1
    for i in range(clients.__len__()):
        Car = car(numOfRoads, "assets\\car.png", screen, width, Road.rect.height, i)
        cars.append(Car)
    for i in range(numOfCars):
        cars.append(car(
            numOfRoads, "assets\\car2.png", screen, width, Road.rect.height, i))

    while display.get_active() and clients.__len__() > 0:
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
            #Car.movement(e)

        data = "0:" + cars[0].speed.__str__() + cars[0].rect.center.__str__()
        for i in range(cars.__len__() - 1):
            data += (";" + (i + 1).__str__() + ":" +
                     cars[i + 1].speed.__str__() + cars[i + 1].rect.center.__str__())
        print(locations)
        for i in range(locations.__len__()):
            if not locations.get(i) == "placeholder":
                location = locations.get(i).split(",")
                cars[i].speed = float(location[0])
                cars[i].rect.center = (
                    int(location[1].strip("(")), int(location[2].strip(")")))
        screen.fill([0, 0, 0])
        # Move the car
        for c in cars:
            try:
                c.rect = c.rect.move(c.speed, 0)
            except:
                print(c.speed)

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
            for C in cars:
                while c.rect.colliderect(C) and not c == C:
                    c.rect.x -= 1
                    C.rect.x += 1
        display.flip()


def menu():
    global simState
    screen.fill((255, 255, 255))
    square = image.load("assets\\start_button.png")
    squarerect = square.get_rect()
    squarerect.center = screen.get_rect().center
    screen.blit(square, squarerect)
    numClients = font.render(
        "total clients: " + clients.__len__().__str__(), True, (0, 0, 0))
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
    for c in clients:
        c.close()
    print("Main thread finished.")


if __name__ == "__main__":
    main()
