import threading
import functions as fcn
import threads

def main():
    fcn.setMode()
    autoThread10 = threading.Thread(target=threads.autoThread10)
    autoThread10.daemon = True
    autoThread10.start()
    autoThread30 = threading.Thread(target=threads.autoThread30)
    autoThread30.start()
    threads.userThread()

main()
