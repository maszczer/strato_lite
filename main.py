import threading
import threads

def main():
    # Thread-1 for APRS.fi
    auto_thread_30_aprs = threading.Thread(target=threads.auto_thread_30_aprs)
    auto_thread_30_aprs.daemon = True
    auto_thread_30_aprs.start()
    # Thread-2 for Ground Station
    auto_thread_10_ground = threading.Thread(target=threads.auto_thread_10_ground)
    auto_thread_10_ground.daemon = True
    auto_thread_10_ground.start()
    # Thread-3 for Prediction and writing log data to output file
    auto_thread_10_else = threading.Thread(target=threads.auto_thread_10_else)
    auto_thread_10_else.daemon = True
    auto_thread_10_else.start()
    # Thread-4 for writing terminal to output file
    auto_thread_30_else = threading.Thread(target=threads.auto_thread_30_else)
    auto_thread_30_else.daemon = True
    auto_thread_30_else.start()
    # Main thread for handling User commands
    threads.user_thread()

main()
