import threading
from socket import *
from Network.client_connection import *

#The following class handles incoming sockets and seperates these into their own threads
class handler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.HOST = ""
        self.PORT = 8888
        self.CONN_COUNTER = 0
        self.running_sockets = []
        self.s = socket(AF_INET, SOCK_STREAM)
        self.data = "placeholder"
        self.locations = {}
        self.simState = False
        self.clients = []
        self.newdata = False
        self.quitting = False
        self.mode = 0 #0 = CACC mode, 1 = Manual mode

#this method is run whenever the start method is called and a thread is created
    def run(self):
        self.s.bind((self.HOST, self.PORT))
        self.s.listen(1)
        while not self.simState:
            c, a = self.s.accept()
            if not self.quitting:
                self.CONN_COUNTER += 1
                #client = client_connection(c,a,self.CONN_COUNTER,self)
                #client.start()
                downlink = Downlink(c, a, self.CONN_COUNTER, self)
                self.running_sockets.append(downlink.start())
                uplink = Uplink(c, a, self.CONN_COUNTER, self)
                uplink.start()
            else:
                break
        print("Socket server finished")

#this method is used to stop the socket server to avoid exceptions, this method simply lets the above code continue from accept
    def stop(self):
        self.quitting = True
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(("127.0.0.1", self.PORT))
        s.send(bytes("quit", 'utf-8'))
        print("stop function called")
        self.s.close()
        s.close()