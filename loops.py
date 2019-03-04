import config as lite
import csv, datetime
import functions as fcn
import numpy as np
import predict, time

def loop_every_10():
    ''' Update data from Ground Station, prediction, and save data to lite.log[] '''

    data = {}
    # Update data from Ground Station
    lite.ground_pos = fcn.get_ground_pos()
    # Check all sources for relevant data
    pos = fcn.get_updated_data(data)
    data['pos'] = pos[0:3]
    data['utime'] = pos[3]
    data['isotime'] = datetime.datetime.now()
    # Update prediction queue
    lite.pred_pos = lite.pred_queue.get()
    lite.pred_queue.put(predict.predict(pos))
    # Calculate AZEL and HADEC values
    hadec = fcn.get_hadec(pos, data)
    # Output data to .csv
    data['ground_pos'] = lite.ground_pos[0:3]
    data['aprs_pos'] = lite.aprs_pos[0:3]
    data['pred_pos'] = lite.pred_pos[0:3]
    # Set command to be sent to telescope
    command = "NOT SET"
    # Minimum elevation for telescope movement is 16 deg
    if data['azel'][1] >= 16 and not np.array_equal(pos, lite.null_pos) and not lite.pause:
        command = "#33," + str(hadec[0]) + "," + str(hadec[1]) + ";"
    data['command'] = command
    lite.log.append(data)
    time.sleep(10)

def loop_every_30():
    ''' Update data from APRS and send command to telescope '''
    time.sleep(30)