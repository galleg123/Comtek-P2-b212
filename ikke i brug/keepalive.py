import threading

class keepalive(threading.Thread):
    def __init__(self):
        threading.Thread.__init__()
    def run(self):
        while True:
            pass