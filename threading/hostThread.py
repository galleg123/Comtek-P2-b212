from socket import AF_INET, SOCK_STREAM, socket
import threading


class socketServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.HOST = ""
        self.PORT = 8888
        self.CONN_COUNTER = 0
        self.running_sockets = []
        self.s = socket(AF_INET, SOCK_STREAM)  # socket

    def run(self):
        self.s.bind((self.HOST, self.PORT))  # bind
        self.s.listen(1)  # listen
        while True:  # loop forever
            c, a = self.s.accept()  # accept
            client = client_connection(c, a)
            self.running_sockets.append(client.start())  # fork


class client_connection(threading.Thread):
    def __init__(self, client, addr):
        threading.Thread.__init__(self)
        self.BUFFER_SIZE = 1024
        self.c = client
        self.r = ""
        print(threading.Thread.getName(self) + " created.")

    def run(self):
        while True:
            self.r = self.c.recv(self.BUFFER_SIZE).decode("utf-8")
            if not self.r == "":
                print(self.r)
                print(threading.Thread.getName(self))
            if self.r == "quit":
                print("returning")
                return


def main():
    s = socketServer()
    s.start()

    print("main thread finished")


if __name__ == "__main__":
    main()
