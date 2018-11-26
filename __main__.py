import threading
import functions as fcn
import threads

def main():
    fcn.setMode()
    autoThread = threading.Thread(target=threads.autoThread)
    #userThread = threading.Thread(target=threads.userThread)
    autoThread.start()
    #userThread.start()
    threads.userThread()

if (__name__ == "__main__"):
    main()

'''
TODO
[x] Add offsets for HA, DEC
[x] Implement offset 'o' to change offset to HA, DEC
[x] set minimum elevation of 16 degrees instead of 18
[x] Change default 'd' to reset 'r' 
[x] Update recurring print for time, aprs data, predicted HA, DEC, any offset, time since last APRS update, etc
[x] Implement data 'd' to print more detailed info for most recent data
[ ] Print error from previous data
[ ] Opt to pull from either GroundStation or APRS, else predicted values
 * Will GroundStation feed dupliacte values if we don't read data? <-- do this
[ ] Write function to determine if getting new data from GroundStation or APRS

NOTE
 * If GPS data is pulled instead of APRS.fi, make sure format is compatible
 * Predicted location is only valid for 1st instance after losing APRS (currently)
 * Predictor will handle offset
'''