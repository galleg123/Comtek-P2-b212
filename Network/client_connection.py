import threading
import time
import tcp_latency


#this class is used whenever a client is connecting to the host, it handles the client
class client_connection(threading.Thread):                                  
    def __init__(self, client, addr, num, handler):                                  
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
            if self.handler.simState:                                                
                if not started:                                         
                    self.c.send(
                        bytes("start,{},{},{}".format(self.num, self.handler.clients.__len__(), self.handler.mode), 'utf-8'))                                      
                    started = True                                      
                if not "placeholder" in self.handler.data:
                    self.c.send(bytes(self.handler.data, 'utf-8'))
                    self.data = self.c.recv(self.BUFFER_SIZE).decode('utf-8')   
                    self.handler.locations[self.num-1] = self.data
                    time.sleep(.00001)

#method to stop the client connection, this is to avoid exceptions
    def close(self):                                                        
        self.c.close()                                                      
        print("closed client connection")                                   