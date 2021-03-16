from socket import *
import pickle


SERVER_IP = "62.107.59.124"
SERVER_PORT = 8888
BUFFER_SIZE = 1024

s = socket(AF_INET, SOCK_STREAM)
s.connect((SERVER_IP, SERVER_PORT))
test = "30"
array = ([1, 2, 3, 4, 5])
dataString = pickle.dumps(array) #Converts array to bytes via pickle

s.send(dataString)
#s.send(bytes(test, "utf-8"))
print("Data sent.")
data = s.recv(BUFFER_SIZE)
print('Received data: {}'.format(data))


