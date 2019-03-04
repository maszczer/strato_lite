import csv, json, math
import numpy as np
import pymap3d as pm
import urllib.request
import config as lite

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
        value = float(data[idx].strip("'"))
    # If no value, then return 0
    except ValueError:
        value = 0
    return value

def get_ground_pos():
    ''' Get latitude, longitude, altitude, and utime from Ground Station .log file '''
    file = open(lite.log_path, 'r')
    row = reversed(list(csv.reader(file)))
    # Ensure .log data read is from the correct callsign
    try:
        while True:
            data = next(row)
            if get_ground_value(data, 3) == lite.ground_callsign:
                lat = get_ground_value(data, 10)
                lng = get_ground_value(data, 11)
                alt = get_ground_value(data, 14)
                utime = get_ground_value(data, 1)
                file.close()
                return [lat, lng, alt, utime]
    # If no data from callsign is found, return null_pos
    except StopIteration:
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

def pos_is_updated(pos, log_data):
    ''' Check if position data from source has updated '''
    # Check if data is null
    if pos == lite.null_pos[0:3]:
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

def get_updated_data(log_data):
    ''' Determine which data source, if any, has updated most recently '''
    # Check current data against null_pos
    if lite.n == 0:
        # Check for new Ground Station data
        if pos_is_updated(lite.ground_pos[0:3], lite.null_pos[0:3]):
            pos = lite.ground_pos
            lite.last_ground_update = 0
            log_data['source'] = "ground"
            # Also check for APRS update
            if pos_is_updated(lite.aprs_pos[0:3], lite.null_pos[0:3]):
                lite.last_aprs_udate = 0
            else:
                lite.last_aprs_udate += 1
        # Else, for new check APRS data
        elif pos_is_updated(lite.aprs_pos[0:3], lite.null_pos[0:3]):
            pos = lite.aprs_pos
            lite.last_aprs_udate = 0
            log_data['source'] = "aprs"
            # Also increment for Ground Station update
            lite.last_ground_update += 1
    # Check current data against previous data
    elif lite.n > 1:
        # Check for new Ground Station data
        if pos_is_updated(lite.ground_pos[0:3], lite.log[lite.n - 1]['ground_pos'][0:3]):
            pos = lite.ground_pos
            lite.last_ground_update = 0
            log_data['source'] = "ground"
            # Also check for APRS update
            if pos_is_updated(lite.aprs_pos[0:3], lite.log[lite.n - 1]['aprs_pos'][0:3]):
                lite.last_aprs_udate = 0
            else:
                lite.last_aprs_udate += 1
        # Else, for new check APRS data
        elif pos_is_updated(lite.aprs_pos[0:3], lite.log[lite.n - 1]['aprs_pos'][0:3]):
            pos = lite.aprs_pos
            lite.last_aprs_udate = 0
            log_data['source'] = "aprs"
            # Also increment for Ground Station update
            lite.last_ground_update += 1
    # If no data is up to date
    else:
        pos = lite.pred_pos
        lite.last_ground_update += 1
        lite.last_aprs_udate += 1
        log_data['source'] = "pred"
    return pos

def get_hadec(pred_pos, log_data):
    ''' Convert position from Geodetic to HADEC '''
    if pos_is_updated(pred_pos[0:3], lite.null_pos[0:3]):
        az, el, range = pm.geodetic2aer(pred_pos[0], pred_pos[1], pred_pos[2],
                                        lite.ref_pos[0], lite.ref_pos[1], lite.ref_pos[2])
        [ha, dec] = azel_to_hadec([az, el, range])
        ha += lite.offset_ha
        dec += lite.offset_dec
    else:
        az = el = range = ha = dec = -404
    log_data['azel'] = [az, el, range]
    log_data['hadec'] = [ha, dec]
    return [ha, dec]