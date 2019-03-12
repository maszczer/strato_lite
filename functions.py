import config as lite
import csv
import json
import math
import numpy as np
import pymap3d as pm
import urllib.request

def azel_to_hadec(azel):
    ''' Converts coordinates from AZ, EL to HA, DEC '''
    a = azel[1]
    z = 90 - a
    A = azel[0]
    phi = lite.ref_pos[0]
    # Python math requires radian values
    z_rad = math.radians(z)
    A_rad = math.radians(A)
    phi_rad = math.radians(phi)
    dec = math.asin(math.cos(z_rad) * math.sin(phi_rad)
                    + math.sin(z_rad) * math.cos(phi_rad) * math.cos(A_rad))
    ha = math.acos(math.cos(z_rad) / (math.cos(dec) * math.cos(phi_rad))
                   - math.tan(dec) * math.tan(phi_rad))
    ha = math.degrees(ha) / 15.0
    dec = math.degrees(dec)
    if azel[0] > 0 and azel[0] < 180:
        ha *= -1
    return [ha, dec]

def get_ground_value(data, idx):
    ''' Get value from row in log data '''
    try:
        value = (data[idx].strip('\n'))
    # If no value, then return 0
    except ValueError:
        value = 0
    return value

def get_ground_pos():
    ''' Get latitude, longitude, altitude, and utime from Ground Station .log file '''
    file = None
    lat = lng = alt = utime = -404
    try:
        file = open(lite.log_path, 'r') #TODO: iterator is not updating
    except FileNotFoundError:
        print("File not found")
        exit(1)
    row = reversed(list(csv.reader(file)))
    # Ensure .log data read is from the correct callsign
    try:
        while True:
            data = next(row)
            # Get data if the correct callsign is found
            try:
                if get_ground_value(data, 3).lower() == lite.ground_callsign.lower():
                    file.close()
                    lat = float(get_ground_value(data, 10))
                    lng = float(get_ground_value(data, 11))
                    alt = float(get_ground_value(data, 14))
                    utime = float(get_ground_value(data, 1))
                    return [lat, lng, alt, utime]
            # Do nothing if row has no callsign
            except ValueError:
                pass
            utime = utime
    # If no data from callsign is found, return null_pos
    except StopIteration:
        file.close()
        return lite.null_pos

def get_aprs_value(json_data, key):
    ''' Get value from JSON data from APRS '''
    try:
        value = json_data['entries'][0][key]
        return value
    # If no value, then return 0
    except KeyError:
        return "0"

def get_aprs_pos():
    ''' Get latitude, longitude, altitude, and utime from APRS '''
    url = "https://api.aprs.fi/api/get?name=" + lite.aprs_callsign + \
          "&what=loc&apikey=" + lite.aprs_key + "&format=json"
    try:
        response = urllib.request.urlopen(url)
    # If URL is invalid
    except ValueError:
        return lite.null_pos
    json_data = json.loads(response.read().decode())
    # Check if JSON from APRS contains data
    if json_data['result'] == "ok":
        try:
            lat = float(get_aprs_value(json_data, 'lat'))
            lng = float(get_aprs_value(json_data, 'lng'))
            alt = float(get_aprs_value(json_data, 'altitude'))
            # Altitude should be stored at ['altitude'], but check for ['alt']
            if alt == 0:
                alt = float(get_aprs_value(json_data, 'alt'))
            utime = get_aprs_value(json_data, 'time')
            return [lat, lng, alt, utime]
        # If no data from callsign is found, return null_pos
        except KeyError:
            return lite.null_pos

def is_pos_updated(pos, log_data):
    ''' Check if position data from source has updated '''
    # Check if data is null
    if np.array_equal(pos, lite.null_pos[0:3]):
        return False
    # Check if data for updates against previous data
    elif lite.n > 0:
        if np.array_equal(pos, log_data):
            return False
        else:
            return True
    # First instance of data will always be up to date
    else:
        return True

#TODO: Debug this
def conditional_data_update(ground_pos, aprs_pos):
    ''' Determine which data source, if any, has updated mosprintt recently '''
    pos = lite.pred_pos
    source = "ground"
    # Check for new Ground Station data
    if is_pos_updated(lite.ground_pos[0:3], ground_pos[0:3]):
        pos = lite.ground_pos
        lite.last_ground_update = 0
        # Also check for APRS update
        if is_pos_updated(lite.aprs_pos[0:3], aprs_pos[0:3]):
            lite.last_aprs_update = 0
        else:
            lite.last_aprs_update += 1
    # Else, check for new APRS data
    elif is_pos_updated(lite.aprs_pos[0:3], aprs_pos[0:3]):
        pos = lite.aprs_pos
        lite.last_aprs_update = 0
        source = "aprs"
        # Also increment for Ground Station update
        lite.last_ground_update += 1
    else:
        lite.last_ground_update += 1
        lite.last_aprs_update += 1
        source = "pred"
    if len(pos) != 4:
        pos.append(-404)
    return pos, source

def get_updated_data(log_data):
    ''' Get updated data from relevant source '''
    pos = lite.pred_pos
    source = "ground"
    # Check current data against null_pos
    if lite.n == 0:
        pos, source = conditional_data_update(lite.null_pos, lite.null_pos)
    # Check current data against previous data
    elif lite.n > 1:
        pos, source = conditional_data_update(lite.log[lite.n - 1]['ground_pos'],
                                              lite.log[lite.n - 1]['aprs_pos'])
    log_data['source'] = source
    return pos

def get_hadec(pred_pos, log_data):
    ''' Convert predicted position from Geodetic to HADEC '''
    if is_pos_updated(pred_pos[0:3], lite.null_pos[0:3]):
        az, el, range = pm.geodetic2aer(pred_pos[0], pred_pos[1], pred_pos[2],
                                        lite.ref_pos[0], lite.ref_pos[1], lite.ref_pos[2])
        [ha, dec] = azel_to_hadec([az, el, range])
        ha += lite.offset_ha
        dec += lite.offset_dec
    else:
        az = el = range = ha = dec = -404
    log_data['azel'] = [az, el, range]
    log_data['hadec'] = [ha, dec]
    log_data['hadec_offset'] = [lite.offset_ha, lite.offset_dec]
    return [ha, dec]

def get_last_pred_pos():
    ''' Return the last predicted geodetic position '''
    if lite.n == 0:
        return lite.null_pos
    else:
        return lite.log[lite.n - 1]['pred_pos']

def is_command_valid(geodetic_pos, elevation):
    ''' Check if next command is valid '''
    # Must be greater than or equal to minimum elevation, non-null, and telescope movement must not be paused
    if elevation >= lite.min_el and not np.array_equal(geodetic_pos, lite.null_pos) and not lite.pause:
        # Might not need to check np.array_equal(geodetic_pos, lite.null_pos)
        return True
    else:
        return False

"""
The following functions are used in place of input() and print()
They will output to a text file in addition to their standard input/output
"""
def input_out(str_prompt):
    ''' Get string input from user and write to output file '''
    lite.output_file.write(str_prompt + "\n")
    str_input = input(str_prompt)
    lite.output_file.write(str_input + "\n")
    return str_input

def print_out(str_input):
    ''' Print and write to output file '''
    lite.output_file.write(str_input + "\n")
    return str_input