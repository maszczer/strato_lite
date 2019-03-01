import threading
import functions as fcn
import threads

def main():
    fcn.setMode()
    autoThread = threading.Thread(target=threads.autoThread)
    autoThread.start()
    threads.userThread()

main()
