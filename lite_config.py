import socket

## GLOBAL VARIABLES ##
mode = "test"
live = 1
pause = 0

print("A valid APRS.fi key is required to begin tracking")
set = 0
while (set == 0):
    aprsKey = input("> Enter registered APRS.fi key\n")
    val = input("Is this correct?\nType 'yes' to confirm, anything else to re-enter\n")
    if (val.lower() == "yes"):
        set = 1

set = 0
print("Geodetic coordinates of telescope required")
while (set == 0):
    lat = input("> Enter telescope latitude (deg)\n")
    lng = input("> Enter telescope longitude (deg)\n")
    alt = input("> Enter telescope altitude (m)\n")
    print("telescope coordinates : [" + lat + ", " + lng + ", " + alt + "]")
    val = input("Is this correct?\nType 'yes' to confirm, anything else to re-enter\n")
    if (val.lower() == "yes"):
        refPos = [float(lat), float(lng), float(alt)]
        set = 1

set = 0
while (set == 0):
    callsign = input("> Enter callsign\n")
    val = input("Is this correct?\nType 'yes' to confirm, anything else to re-enter\n")
    if (val.lower() == "yes"):
        set = 1

# timer is reduced by 2 seconds
# to account for the 2 instances of time.sleep() in lite_functions.repeat()
set = 0
while (set == 0):
    timer = int(input("> Enter time (sec) between each update (minimum time is 5 seconds)\n"))
    if (timer < 5):
        print("Invalid time\n")
    else:
        timer -= 2
        set = 1

# data logged from APRS
log = []

# data logged for use by telescope
# if APRS does not update, predicted location will be used
predLog = []

# number of iterations since last APRS update
noUpdate = 0

n = 0
offsetHA = 0.00
offsetDEC = 0.00

# printed indicates if any data has been pulled
# error will occur when calling 'data' or 'status' before any data has been pulled
printed = 0

# string output sent to telescope

# socket for sending commands in tracking_ACTUAL
TCP_IP = ""
TCP_PORT = ""
sock = None