import queue, socket

## HELPER FUNCTIONS ##
def enforce_float(value, value_name):
    ''' Exit 1 if input is not float '''
    try:
        return float(value)
    except ValueError:
        print("Error: " + value_name + " must be a float")
        exit(1)

def enforce_int(value, value_name):
    ''' Exit 1 if input is not float '''
    try:
        return int(value)
    except ValueError:
        print("Error: " + value_name + " must be an int")
        exit(1)

def get_input_file(filename):
    ''' Get input variables from .txt file '''
    file = open(filename, 'r')
    data = file.splitlines()
    aprs_key = data[0]
    # Only lat, lng, alt stored as float
    lat = enforce_float(data[1], "latitude")
    lng = enforce_float(data[2], "longitude")
    alt = enforce_float(data[3], "altitude")
    # Other values are string
    aprs_callsign = ground_callsign = TCP_IP = TCP_PORT = log_path = None
    values = [
        aprs_callsign,
        ground_callsign,
        TCP_IP,
        TCP_PORT,
        log_path
    ]
    for i in range(4,9):
        values[i - 4] = data[i]
    file.close()
    return aprs_key, [lat, lng, alt], aprs_callsign, ground_callsign, TCP_IP, TCP_PORT, log_path

def tcp_connect(ip_addr, port):
    ''' Connect to telescope over TCP/IP, if possible '''
    # If IP Address and Port Number are NOT SET, continue without setting up socket
    if ip_addr == "NOT SET" and port == "NOT SET":
        print("TCP/IP connection not specified\n"
              "No commands will be sent\n")
    # Try to set up socket
    else:
        port_number = enforce_int(port, "TCP/IP Port Number")
        try:
            sock = socket.socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip_addr, port_number))
            print("Connection established ....\n")
        # If the specified IP Address and Port Number are not listening for TCP/IP packets
        except ConnectionRefusedError:
            confirm = input("Failed to connect, no commands will be sent\n"
                            "Would you still like to continue?\n"
                            "Type 'yes' to continue, anything else to quit\n")
            if confirm.replace(" ", "") == "yes".lower():
                exit(1)

def init_pred_queue():
    ''' Initialize queue for 30 sec predictions '''
    pred_queue = queue.Queue()
    for i in range(3):
        pred_queue.put(null_pos)
    return pred_queue

# Get data from input file
aprs_key, ref_pos, aprs_callsign, ground_callsign,\
TCP_IP, TCP_PORT, log_path = get_input_file(input("Enter input filename"))

# Try connecting to telescope over TCP/IP
tcp_connect(TCP_IP, TCP_PORT)

# Set control variables
live = True
pause = False

# Current iteration, 10 sec interval
n = 0

# Ensures data has been acquired before accessing
printed = False

'''
log is a list containing data stored throughout the flight
----------------------------------------------------------
Each instance in the list will store a dictionary
containing the following elements:
    pos[]: stores [latitude, longitude, altitude] sent to telescope
    azel[]: stores [azimuth, elevation, range]
    hadec[]: stores [hourAngle, declination]
    grnd_pos[]: stores [latitude, longitude, altitude] from Ground Station
    aprs_pos[]: stores [latitude, longitude, altitude] from APRS.fi
    pred_pos[]: stores predicted [latitude, longitude, altitude]
    utime: timestamp from Ground Station or APRS packets
    isotime: timestamp from the user's system
    commmand: string sent to the telescope
    source: string for determining source of pos used
'''
log = []

# Null position data
null_pos = [-404, -404, -404, -404]

# Latest position data
ground_pos = null_pos
aprs_pos = null_pos
pred_pos = null_pos

# Store 30 sec predictions in queue
pred_queue = init_pred_queue()

# Number of iterations since last update
last_ground_update = 0
last_aprs_udate = 0

# Manual offset
offset_ha = 0
offset_dec = 0