from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket
import time

clients:list[socket] = []

def main():
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(("", 8888))
    s.listen(1)
    print("listening for connections")
    for i in range(5):
        client,addr = s.accept()
        print("accepted client from {}".format(addr))
        clients.append(client)
    while True:
        for client in clients:
            client.send(bytes("hello world!","utf-8"))
        time.sleep(1/30)

if __name__ == "__main__":
    main()

