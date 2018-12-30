import threading
import functions as fcn
import threads

def main():
    fcn.setMode()
    grndThread = threading.Thread(target=threads.grndThread)
    grndThread.daemon = True
    grndThread.start()
    autoThread = threading.Thread(target=threads.autoThread)
    autoThread.start()
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
[x] Opt to pull from either GroundStation or APRS, else predicted values
 * Will GroundStation feed dupliacte values if we don't read data? <-- do this
[x] Write function to determine if getting new data from GroundStation or APRS
[x] predPos logs prediction for 30 sec into future
[ ] Write test script for predict.py
[x] Change timer b/c groundstation pulls every 10s, APRS will be every 20s
    Hard code timer to 10s

NOTE
 * If GPS data is pulled instead of APRS.fi, make sure format is compatible
 * Predicted location is only valid for 1st instance after losing APRS (currently)
 * Predictor will handle automated offset
 * Pos[] data will be determined using descending priority as follows:
    grndPos[]   --> predict(grndPos[])
    aprsPos[]   --> predict(aprsPos[])
    predPos[]   --> predict(predPos[])
    else            #12;
   Use if/elif blocks
'''