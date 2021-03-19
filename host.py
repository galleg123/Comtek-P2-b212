from socket import AF_INET, SOCK_STREAM, socket
import socketserver
import sys
import threading
from Network.thread import uploadThread

from classes.car import car
from classes.road import road
from pygame import KEYDOWN, MOUSEBUTTONDOWN, TEXTINPUT, image, display, init, event, QUIT, transform, mouse, font

init()                              #initialize pygame module
size = width, height = 1920, 1000   #create a window size
screen = display.set_mode(size)     #set the pygame window to the window size
clients = []                        #create a list of all clients
simState = False                    #global variable to determine if the simulation is running
font = font.Font("freesansbold.ttf", 32)    #create a font object used in the window

data = "placeholder"        #create a placeholder string for sent data
locations = {}              #create an empty dictionary to save received data in

#The following class handles incoming sockets and seperates these into their own threads
class socketServer(threading.Thread):   #class definition, this class inherits from the threading module
    def __init__(self):                 #method called when the object is initialized
        threading.Thread.__init__(self) #when the object is initialized, initialize the thread itself
        self.HOST = ""                  #create an empty variable for the socket
        self.PORT = 8888                #define a port to be accessed by the clients
        self.CONN_COUNTER = 0           #variable to count connections
        self.running_sockets = []       #list to save each socket instance to
        self.s = socket(AF_INET, SOCK_STREAM)  #create a socket for incoming connections

#this method is run whenever the start method is called and a thread is created
    def run(self):      #define the method
        self.s.bind((self.HOST, self.PORT))  #bind the socket to host on a specific port
        self.s.listen(1)            #listen for incoming connections
        while not simState:         #loop until game is executed
            c, a = self.s.accept()  #accept a connection when a client is trying to join
            self.CONN_COUNTER += 1  #count the amount of clients connected
            client = client_connection(c, a, self.CONN_COUNTER) #create a thread object for the connection
            self.running_sockets.append(client.start()) #fork the connection onto its own thread and continue the loop
        print("Socket server finished")                 #debug

#this method is used to stop the socket server to avoid exceptions, this method simply lets the above code continue from accept
    def stop(self):     #method definition
        s = socket(AF_INET, SOCK_STREAM)    #create a tcp socket
        s.connect(("127.0.0.1", self.PORT)) #connect to localhost
        s.send(bytes("quit", 'utf-8'))      #send a message telling the socket to quit the connection
        s.close()                           #close the socket

#this class is used whenever a client is connecting to the host, it handles the client
class client_connection(threading.Thread):  #define the class, it inherits from threading
    def __init__(self, client, addr, num):  #initialize the object
        threading.Thread.__init__(self)     #initialize the thread
        self.BUFFER_SIZE = 1024             #create buffer variable to set an amount of data to get each time it's receiving
        self.c = client                     #save the received socket
        self.r = ""                         #create variable for received data
        self.addr = addr                    #save received ipv4 address
        self.num = num                      #give the client the received number
        print(threading.Thread.getName(self) + " created.")     #debug

#this method is run whenever the start method is used
    def run(self):          #define the method
        global data         #import the global variable data
        global locations    #import locations
        try:                #try statement to let the user know if an exception occurs
            while True:     #infinite while loop running as long as there is a connection
                self.r = self.c.recv(self.BUFFER_SIZE).decode("utf-8")      #receive some encoded data from the client and decode it
                if self.addr[0] == "127.0.0.1":                             #if the data is received from localhost
                    return                                                  #then return from the method, it can only be a quit event
                elif not self.r == "":                                      #if received data is not emtry
                    print(self.r)                                           #debug
                    if self.r == "join":                                    #if the received data is join
                        clients.append(self)                                #then add the client to the list of clients 
                        break                                               #break out of the loop
                elif self.r == "quit":                                      #if the message is quit
                    print("Client on " + threading.Thread.getName(self) +   #debug
                          " ended the connection by keyword.")
                    return                                                  #then return from the method and stop the thread
            started = False             #when the following loop is run, the simulation shouldn't have started yet, used to ensure the start keyword is only sent once
            while True:                 #infinite loop
                if simState:            #if the simulation is run
                    if not started:     #if this client hasn't started their simulation
                        self.c.send(
                            bytes("start," + self.num.__str__(), 'utf-8'))  #send a message telling it to start
                        print("start")                                      #debug
                        started = True                                      #never run this code again
                    self.c.send(bytes(data, 'utf-8'))                       #send the location data to the client
                    self.data = self.c.recv(self.BUFFER_SIZE).decode('utf-8')   #get data from the client, this is run now because either the client or server has to go first
                    locations[self.num-1] = self.data                       #save the data to global dictionary with a keyword identifier

        except:         #if there is an exception of any kind
            print("Client on " + threading.Thread.getName(self) +
                  " ended the connection by exception (close window).")     #print the reason this probably happened
            return      #return from the method and stop the thread

#method to stop the client connection, this is to avoid exceptions
    def close(self):                        #method definition
        self.c.close()                      #close the socket
        print("closed client connection")   #debug


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

    Car = car(numOfRoads, "assets\\car.png", screen, width, Road.rect.height)
    cars.append(Car)
    for i in range(numOfCars):
        cars.append(car(
            numOfRoads, "assets\\car2.png", screen, width, Road.rect.height))

    while display.get_active():
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
            Car.movement(e)

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
        for i in range(cars.__len__()):
            try:
                cars[i].rect = cars[i].rect.move(cars[i].speed, 0)
            except:
                print(cars[i].speed)

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
