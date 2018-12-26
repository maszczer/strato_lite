"""
Setup variables to be used globally throughout program
"""

## HELPER FUNCTIONS ##
''' Return true if string is a numerical value '''
def checkNum(strIn):
    try:
        float(strIn)
        return True
    except ValueError:
        return False

''' Generic value for setting variable's value from user input '''
def setVar(varStr):
    while True:
        var = input("> Enter " + varStr + "\n")
        confirm = input("Is this correct?\n"
                        "Type 'yes' to confirm, anything else to re-enter\n")
        if confirm.lower() == "yes":
            break

    return var

''' Set reference position (geodetic) from user input '''
def setRefPos():
    refPos = []
    print("Geodetic coordinates of telescope required")
    while True:
        lat = input("> Enter telescope latitude (deg)\n")
        lng = input("> Enter telescope longitude (deg)\n")
        alt = input("> Enter telescope altitude (m)\n")
        if checkNum(lat) and checkNum(lng) and checkNum(alt):
            print("Telescope coordinates : [" + lat + ", " + lng + ", " + alt + "]")
            confirm = input("Is this correct?\n"
                            "Type 'yes' to confirm, anything else to re-enter\n")
            if confirm.lower() == "yes":
                refPos = [float(lat), float(lng), float(alt)]
                break
        else:
            print("Latitude, longitude, and altitude must be numbers\n")

    return refPos



## GLOBAL VARIABLES ##
mode = "test"
live = True
pause = False

# APRS key
print("A valid APRS.fi key is required to begin tracking")
aprsKey = setVar("a registered APRS.fi key")

# Reference Position (geodetic)
refPos = setRefPos()

# Callsign to track
callsign = setVar("callsign")

'''
log is a list containing data stored throughout the flight
----------------------------------------------------------
Each instance in the list will store a dictionary
containing the following elements:
    pos[]: stores [latitude, longitude, altitude] sent to telescope
    azel[]: stores [azimuth, elevation, range]
    hadec[]: stores [hourAngle, declination]
    grndPos[]: stores [latitude, longitude, altitude] from Ground Station
    aprsPos[]: stores [latitude, longitude, altitude] from APRS.fi
    predPos[]: stores predicted [latitude, longitude, altitude]
    aprsTime: timestamp from the APRS packet
    userTime: timestamp from the user's system
    commmand: string sent to the telescope
    source: string for determining source of pos used
'''
log = []

# number of iterations since last APRS update
noUpdate = 0

# Current iteration
n = 0

# Manually added offset
offsetHA = offsetDEC = 0.00

# Indicates if any data has been pulled
# An error will occur when calling 'data' or 'status' before any data has been pulled
printed = False

# socket for sending commands in tracking_ACTUAL
TCP_IP = TCP_PORT = "Not set"
sock = None
