import pickle
from socket import *
import sys
import threading
import time


class uploadThread(threading.Thread):
    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data

    def run(self):
        print("uploading")
        SERVER_IP = "62.107.59.124"
        SERVER_PORT = 8888
        BUFFER_SIZE = 1024

        s = socket(AF_INET, SOCK_STREAM)
        s.connect((SERVER_IP, SERVER_PORT))
        test = "30"
        dataString = pickle.dumps(self.data)                  # Konverter array til bytes via pickle

        s.send(dataString)                                    #s.send(bytes(test, "utf-8"))
        print("Data sent.")
        time.sleep(1)
        s.close()
