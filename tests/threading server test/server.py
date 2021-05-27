import threading
from socket import AF_INET, SOCK_STREAM, socket
import time



class downlink(threading.Thread):
    def __init__(self, s:socket):
        threading.Thread.__init__(self)
        self.s = s
    def run(self):
        pass

class uplink(threading.Thread):
    def __init__(self, s:socket):
        threading.Thread.__init__(self)
        self.s = s
    def run(self):
        while True:
            self.s.send(bytes("hello world!", "utf-8"))
            time.sleep(1/30)

threads:list[tuple[downlink, uplink]] = []

def main():
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(("", 8888))
    server.listen(1)
    for i in range(5):
        client, addr = server.accept()
        threads.append((downlink(client), uplink(client)))
        threads[len(threads)-1][0].start()
        threads[len(threads)-1][1].start()

if __name__ == "__main__":
    main()