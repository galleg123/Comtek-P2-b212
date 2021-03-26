from socket import *
import threading
from Network.thread import uploadThread

from classes.car import car
from classes.road import road
from pygame import TEXTINPUT, image, display, init, event, QUIT, transform

#Global variables
data = "placeholder"                                                        #variable with a placeholder value to be uploaded to the server
locations = {}                                                              #Dictionary which is accessed for the purposes of synchronizing all clients
clientNum = 0                                                               #The specific number each client has
clients = 0

# seperate thread to keep the connection to the server going while the simulation is running
class client(threading.Thread):                                             #class definition, inherits from the threading class
    def __init__(self):                                                     #initialisation method which is run when class is initialized
        threading.Thread.__init__(self)                                     #when the object itself is initialized, initialize the thread
        #self.SERVER_IP = "192.168.0.100"                                    #String containing the IP address of the host server
        self.SERVER_IP = "62.107.59.124"
        self.SERVER_PORT = 8888                                             #Integer containing the port number of the host server
        self.BUFFER_SIZE = 1024                                             #buffer size determining how much data is read at a time
        self.s = socket(AF_INET, SOCK_STREAM)                               #the socket object is created
        self.s.connect((self.SERVER_IP, self.SERVER_PORT))                  #Connects the socket to the server IP on the specific port

#Method that is run when the thread is started
    def run(self):                                                          #method definition
        global data                                                         #Import the global variable data
        global locations                                                    #Import locations
        global clientNum                                                    #Import clientNum
        global clients
        self.joined = False                                                 #create local variable to determine if the client has joined the session
        while True:                                                         #run an infinite loop until broken out of or returned
            In = input("write join to join a session: ")                    #wait until user writes a string into the terminal
            if In.__len__() > 0:                                            #check if the received string isn't empty
                self.s.send(bytes(In, 'utf-8'))                             #send the string to the host server
                print("data sent.")                                         #debug
            if In == "join":                                                #if the sent string is join, do the following
                self.joined = True                                          #set local boolean to true
                break                                                       #break out of the infinite loop and continue to the simulation
            if In == "quit":                                                #if the sent string is quit do the following
                self.s.close()                                              #close socket
                return                                                      #return out of the socket, this is to avoid exceptions when closing the window

        self.started = False                                                #local variable used to determine whether the host has started the simulation or not
        while self.joined:                                                  #run while loop while the client is connected
            r = self.s.recv(self.BUFFER_SIZE).decode('utf-8')               #receive an encoded string from the host server and decode it
            if not r == "placeholderplaceholder" and not r.split(",")[0] == "start":    #check if it's a placeholder or another keyword
                #print(r)
                dataArray = r.split(";")                                    #decode the string into an array of dictionary formatted variables
                for d in dataArray:                                         #run for loop for every entry in the array
                    locations[int(d.split(":")[0])] = d.split(":")[1]       #seperate each array entry into key and value pairs and create a dictionary
            if r.split(",")[0] == "start":                                  #if the received data is start followed by a seperator
                clientNum = r.split(",")[1]                                 #set client number to the number after the seperator
                clients = int(r.split(",")[2])
                self.started = True                                         #set local variable for determining simulation state to true
            if data.__len__() > 0:                                          #if there is data to send to the host server, send it
                self.s.send(bytes(data, 'utf-8'))                           #send the data to the host server

    #method that is called to close the connection and stop the program, used to avoid exceptions
    def stop(self):                     #method definition
        self.s.close()                  #close the socket
        self.joined = False             #set local variable to false



def simulation():
    global clientNum
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
    for i in range(clients):
        cars.append(car(numOfRoads, "assets\\car.png", screen, width, Road.rect.height))
    for i in range(numOfCars):
        cars.append(car(
            numOfRoads, "assets\\car2.png", screen, width, Road.rect.height))
    Car = cars[0]

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
        if locations.__len__() == cars.__len__():
            for i in range(1, cars.__len__()):
                location = locations[i].split("(")
                print(location)
                cars[i].speed = float(location[0])
                cars[i].rect.center = (int(location[1].strip(")").split(
                    ",")[0]), int(location[1].strip(")").split(",")[1]))
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
            for C in cars:
                while c.rect.colliderect(C) and not c == C:
                    c.rect.x -= 1
                    C.rect.x += 1
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
