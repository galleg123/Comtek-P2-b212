from socket import *
import threading


class client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.SERVER_IP = "192.168.0.100"
        self.SERVER_PORT = 8888
        self.BUFFER_SIZE = 1024
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((self.SERVER_IP, self.SERVER_PORT))

    def run(self):
        while True:
            In = input("write something: ")
            if In.__len__() > 0:
                self.s.send(bytes(In, 'utf-8'))
                print("data sent.")
            if In == "quit":
                self.s.close()
                return


def main():
    c = client()
    c.start()
    print("main thread finished")


if __name__ == "__main__":
    main()
