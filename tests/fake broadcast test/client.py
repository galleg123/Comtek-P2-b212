from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket


def main():
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.connect(("127.0.0.1", 8888))
    print("connection established")
    while True:
        r = s.recv(1024).decode()
        print("received {}".format(r))

if __name__ == "__main__":
    main()