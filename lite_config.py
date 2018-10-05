import socket

# Checks if string contains only a numeric value
def checkNum(strIn):
    try:
        float(strIn)
        return 1
    except ValueError:
        return 0

## GLOBAL VARIABLES ##
mode = "test"
live = 1
pause = 0

# APRS key
print("A valid APRS.fi key is required to begin tracking")
aprsKey = ""; set = 0
while (set == 0):
    aprsKey = input("> Enter registered APRS.fi key\n")
    val = input("Is this correct?\nType 'yes' to confirm, anything else to re-enter\n")
    if (val.lower() == "yes"):
        set = 1

# Reference position (geodetic)
refPos = []; set = 0
print("Geodetic coordinates of telescope required")
while (set == 0):
    lat = input("> Enter telescope latitude (deg)\n")
    lng = input("> Enter telescope longitude (deg)\n")
    alt = input("> Enter telescope altitude (m)\n")
    if ((checkNum(lat) == 1) & (checkNum(lng) == 1) & (checkNum(alt) == 1) ):
        print("telescope coordinates : [" + lat + ", " + lng + ", " + alt + "]")
        val = input("Is this correct?\nType 'yes' to confirm, anything else to re-enter\n")
        if (val.lower() == "yes"):
            refPos = [float(lat), float(lng), float(alt)]
            set = 1
    else:
        print("Latitude, longitude, & altitude must be numbers\n")

# Callsign to track
callsign = ""; set = 0
while (set == 0):
    callsign = input("> Enter callsign\n")
    val = input("Is this correct?\nType 'yes' to confirm, anything else to re-enter\n")
    if (val.lower() == "yes"):
        set = 1

# Time between calls to APRS
# Timer is reduced by 2 seconds to account for
# the 2 instances of time.sleep() in lite_functions.repeat()
timer = 0; set = 0
while (set == 0):
    timer = input("> Enter time (sec) between each update (minimum time is 5 seconds)\n")
    if (checkNum(timer) == 1):
        timer = float(timer)
        if (timer < 5):
            print("Interval is too short\n")
        else:
            timer -= 2
            set = 1
    else:
        print("Input must be a number\n")

# Data is stored in in log as a list [0:14]
# [lat, lng, alt, time, timestamp, az, el, range, ha, dec, strOut, predLat, predLng, predAlt, source]
# for each call to APRS
# NOTE: strOut is the string sent to the telescope for a given call
log = []

# number of iterations since last APRS update
noUpdate = 0

n = 0
offsetHA = 0.00
offsetDEC = 0.00

# printed indicates if any data has been pulled
# error will occur when calling 'data' or 'status' before any data has been pulled
printed = 0

# socket for sending commands in tracking_ACTUAL
TCP_IP = "Not set"
TCP_PORT = "Not set"
sock = None