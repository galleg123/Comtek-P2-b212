from socket import socket
import threading
import time
import tcp_latency

lock = threading.Lock()
#this class is used whenever a client is connecting to the host, it handles the client
class client_connection(threading.Thread):         
    def __init__(self, client: socket, addr: str, num: int, handler):
        threading.Thread.__init__(self)
        self.BUFFER_SIZE = 1024
        self.c = client   
        self.r = ""       
        self.addr = addr  
        self.num = num    
        self.handler = handler
        print(threading.Thread.getName(self) + " created.")

#this method is run whenever the start method is used
    def run(self):          
        while True:   
            self.r = self.c.recv(self.BUFFER_SIZE).decode("utf-8")      
            if self.r == "quit":
                print("Client on " + threading.Thread.getName(self) + " ended the connection by keyword.")
                return
            elif not self.r == "":             
                print("received: {}".format(self.r))                  
                if self.r == "join":           
                    print("latency: {}".format(tcp_latency.measure_latency(host="127.0.0.1",port=8888, runs=1,timeout=2.5,wait=0)))
                    self.handler.clients.append(self)        
                    break             
        started = False                        
        while True:
            self.c.settimeout(1)
            lastdata = "placeholder"
            if self.handler.simState:                       
                if not started:                
                    self.c.send(
                        bytes("start,{},{},{}".format(self.num, self.handler.clients.__len__(), self.handler.mode), 'utf-8'))             
                    started = True             
                if not "placeholder" in self.handler.data and self.handler.data != lastdata:
                    self.c.send(bytes(self.handler.data, 'utf-8'))
                    lastdata = self.handler.data
                    try:
                        print("received data")
                        self.r = self.c.recv(self.BUFFER_SIZE).decode("utf-8")
                        self.handler.locations[self.num-1] = self.r
                        self.handler.newdata = True
                    except:
                        continue

#method to stop the client connection, this is to avoid exceptions
    def close(self):      
        self.c.close()    
        if self.handler.clients.count(self) > 0:
            self.handler.clients.remove(self)
        print("clients still present: {}".format(self.handler.clients.__len__()))
        print("closed client connection")


#rewrite using a real event based system
#this first class handles the incoming traffic received from any client connected
class Downlink(threading.Thread):
    bufferSize = 1024

    def __init__(self, socket: socket, addr: str, num: int, handler):
        threading.Thread.__init__(self)
        self.socket = socket
        self.addr = addr
        self.num = num
        self.handler = handler
    def run(self):
        joined = False
        while not joined:
            try:
                lock.acquire()
                r = self.socket.recv(self.bufferSize).decode("utf-8")
                lock.release()
            except:
                lock.release()
                print("timed out")

            if r == "quit":
                print("Client on " + threading.Thread.getName(self) + " ended the connection by keyword.")
                return
            elif r != "":
                print("received: {}".format(r))
                if r == "join":
                    print("latency: {}".format(tcp_latency.measure_latency(host="127.0.0.1",port=8888, runs=1,timeout=2.5,wait=0)))
                    self.handler.clients.append(self)
                    joined = True
                    break
        while True:
            if self.handler.simState:
                try:
                    r = self.socket.recv(self.bufferSize).decode("utf-8")
                    print("received data: {}".format(r))
                    self.handler.locations[self.num-1] = r
                    self.handler.newdata = True
                except:
                    print("timed out")
                    continue
    def close(self):
        self.socket.close()
        if self.handler.clients.count(self) > 0:
            self.handler.clients.remove(self)
        self.handler.data = "quit"
        print("clients still present: {}".format(self.handler.clients.__len__()))
        print("closed client connection")



#this class will handle all sent data to the clients
class Uplink(threading.Thread):
    def __init__(self, socket: socket, addr: str, num: int, handler):
        threading.Thread.__init__(self)
        self.socket = socket
        self.addr = addr
        self.handler = handler
        self.num = num
    def run(self):
        started = False
        running = True
        lastdata = "placeholder"
        while running:
            if self.handler.simState:
                if not started:
                    self.socket.send(bytes("start,{},{},{}".format(self.num, self.handler.clients.__len__(), self.handler.mode), "utf-8"))
                    started = True
                elif not "placeholder" in self.handler.data and self.handler.data != lastdata:
                    print("sending data")
                    lock.acquire()
                    self.socket.send(bytes(self.handler.data, 'utf-8'))
                    lock.release()
                    lastdata = self.handler.data
                if "quit" in self.handler.data:
                    print("quitting uplink")
                    return
            else:
                time.sleep(1)