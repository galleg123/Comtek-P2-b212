import threading
from socket import *

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

#Method that is run when the thread is started
    def run(self):
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
            if not "placeholder" in r and not r.split(",")[0] == "start":
                dataArray = r.split(";")                                    
                for d in dataArray:
                    self.locations[int(d.split(":")[0])] = d.split(":")[1]       
            if r.split(",")[0] == "start":                                  
                self.clientNum = int(r.split(",")[1]) -1                         
                self.clients = int(r.split(",")[2])
                self.mode = int(r.split(",")[3]) #0 = CACC, 1 = Manual
                self.started = True                                         
            if self.data.__len__() > 0:                                          
                self.s.send(bytes(self.data, 'utf-8'))

    #method that is called to close the connection and stop the program, used to avoid exceptions
    def stop(self):                     
        self.s.close()                  
        self.joined = False             