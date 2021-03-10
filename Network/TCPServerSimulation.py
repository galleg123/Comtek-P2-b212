from socket import *
import pickle, mysql.connector

mydb = mysql.connector.connect(
  host="62.107.59.124",
  user="remote",
  password="test"
)
mycursor = mydb.cursor()

HOST = ''           # Symbolic name meaning all available interfaces
PORT = 8888         # Arbitrary non-privileged port
CONN_COUNTER = 0    # Counter for connections
BUFFER_SIZE = 1024  # Receive Buffer size (power of 2)

s = socket(AF_INET, SOCK_STREAM)  # IPv4, TCP
s.bind((HOST, PORT))    # Bind socket to the address
s.listen(1)             # Listen for connections on the socket (0-5)

print('* TCP Server listening for incoming connections in port {}'.format(PORT))

while True:  # Server infinite loop
    CONN_COUNTER = CONN_COUNTER + 1
    c, a = s.accept()    # Accepts a connection,
    # c is a new socket object usable to send and receive data on the connection
    # a is the address bound to the socket on the other end of the connection
    print('* Connection {} received from {}'.format(CONN_COUNTER, a))
    r = c.recv(BUFFER_SIZE)
    ##print('\tIncoming text: {}'.format(r))
    dataArray = pickle.loads(r) #Konverter fra bytes til det originale array
    print('\tIncoming text: {}'.format(dataArray))
    c.send(bytes('Hi there! Got your message from {} Number {}'.format(a[0], CONN_COUNTER), 'utf-8'))
    c.close()

    print(dataArray[0])

    mycursor.execute("INSERT INTO test.testtable VALUES (%s, %s, %s, %s, %s, %s);", (str.join(a), dataArray[0], dataArray[1], dataArray[2], dataArray[3], dataArray[4], ))
    mycursor.execute("COMMIT;")
    print("Inserted into table \n")


