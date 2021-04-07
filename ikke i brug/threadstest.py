import threading
import time


class myThread(threading.Thread):
    def __init__(self, threadID, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.delay = delay

    def run(self):
        time.sleep(self.delay)
        print("thread: " + self.threadID.__str__())


def main():
    thread1 = myThread(1, 1)
    thread2 = myThread(2, 2)

    thread1.start()
    thread2.start()
    print("main thread executed")


if __name__ == "__main__":
    main()
