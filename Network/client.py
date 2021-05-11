import threading
from socket import *
import time

# seperate threads to keep the connection to the server going while the simulation is running
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
                #print(r)
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
                self.socket.sendall(bytes(self.data, "utf-8"))
                self.lastdata = self.data