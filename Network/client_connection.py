from socket import socket
import threading
import time
import tcp_latency

lock = threading.Lock()
#this class is used whenever a client is connecting to the host, it handles the client

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
        print(threading.Thread.getName(self) + " downlink created.")

    def run(self):
        self.handler.clients.append(self)
        print("latency: {}".format(tcp_latency.measure_latency(host=self.addr[0],port=8888, runs=1,timeout=2.5,wait=0)))
        while True:
            if self.handler.simState:
                try:
                    r = self.socket.recv(self.bufferSize).decode("utf-8")
                    self.handler.locations[self.num-1] = r
                    self.handler.newdata = True
                except:
                    #print("timed out")
                    continue
            elif self.handler.data == "quit":
                break
        print("downlink on {} finished".format(threading.Thread.getName(self)))
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
        print(threading.Thread.getName(self) + " uplink created.")
    def run(self):
        started = False
        running = True
        lastdata = "placeholder"
        while running:
            if self.handler.simState:
                if not started:
                    self.socket.sendall(bytes("start,{},{},{}".format(self.num, self.handler.clients.__len__(), self.handler.mode), "utf-8"))
                    started = True 
                elif not "placeholder" in self.handler.data and self.handler.data != lastdata:
                    self.socket.sendall(bytes(self.handler.data, 'utf-8'))
                    lastdata = self.handler.data
                if "quit" in self.handler.data:
                    print("quitting uplink")
                    break
            else:
                time.sleep(1)
        print("Uplink on {} finished".format(threading.Thread.getName(self)))