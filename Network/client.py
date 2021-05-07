import threading
from socket import *
import time

# seperate thread to keep the connection to the server going while the simulation is running
class client(threading.Thread):                                             
    def __init__(self):                                                     
        threading.Thread.__init__(self)  
        #self.SERVER_IP = "85.191.151.221"                                  #rasmus     
        #self.SERVER_IP = "10.225.171.52"                                   #thomas
        #self.SERVER_IP = "62.107.59.124"                                   #kenneth
        #self.SERVER_IP = "192.168.1.45"                                    #mikkel
        #self.SERVER_IP = "192.168.50.206"                                  #christian
        self.SERVER_IP = "127.0.0.1"                                        #localhost, use this for debug

        self.SERVER_PORT = 8888                                             
        self.BUFFER_SIZE = 1024                                             
        self.s = socket(AF_INET, SOCK_STREAM)                               
        self.s.connect((self.SERVER_IP, self.SERVER_PORT))     
        self.data = "placeholder"
        self.locations = {}             
        self.clientNum = 0
        self.clients = 0
        self.newdata = False

#Method that is run when the thread is started
    def run(self):
        self.joined = False
        lastdata = "placeholder"
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
            if self.data.__len__() > 0 and self.data != lastdata:
                self.s.send(bytes(self.data, 'utf-8'))
                lastdata = self.data
            try:
                r = self.s.recv(self.BUFFER_SIZE).decode('utf-8')
                print("received data: {}".format(r))
                self.newdata = True
            except:
                r = "placeholder"
                print("timed out")
                continue
            if not "placeholder" in r and not r.split(",")[0] == "start":
                dataArray = r.split(";")
                for d in dataArray:
                    self.locations[int(d.split(":")[0])] = d.split(":")[1]       
            if r.split(",")[0] == "start":
                self.clientNum = int(r.split(",")[1]) -1
                self.clients = int(r.split(",")[2])
                self.mode = int(r.split(",")[3]) #0 = CACC, 1 = Manual
                self.started = True
                self.s.settimeout(1)


    #method that is called to close the connection and stop the program, used to avoid exceptions
    def stop(self):                     
        self.s.close()                  
        self.joined = False

class Downlink(threading.Thread):
    def __init__(self, socket: socket):
        threading.Thread.__init__(self)
        self.joined = False
        self.socket = socket
        self.lastdata = "placeholder"
        self.locations = {}
        self.bufferSize = 1024
        self.started = False
        self.newdata = False

    def run(self):
        print("downlink running")
        while True:
            try:
                r = self.socket.recv(self.bufferSize).decode("utf-8")
                print(r)
            except:
                print("timed out")
                continue
            if not self.started and "start" in r:
                print("start received")
                self.clientNum = int(r.split(",")[1]) -1
                self.clients = int(r.split(",")[2])
                self.mode = int(r.split(",")[3]) #0 = CACC, 1 = Manual
                self.started = True
            elif self.started:
                if not "placeholder" in r and not "start" in r and len(r) > 0:
                    for data in r.split(";"):
                        try:
                            self.locations[int(data.split(":")[0])] = data.split(":")[1]
                        except:
                            print(data)
                            continue
                    
        

class Uplink(threading.Thread):
    def __init__(self,socket: socket):
        threading.Thread.__init__(self)
        self.socket = socket
        self.data = "placeholder"
        self.lastdata = "placeholder"
    def run(self):
        print("uplink running")
        while True:
            if not "placeholder" in self.data and self.data != self.lastdata:
                self.socket.send(bytes(self.data, "utf-8"))
                self.lastdata = self.data