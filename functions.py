"""
Functions shared by LITE files
"""
import datetime, math, socket
import numpy as np
import pymap3d as pm
import time, urllib.request
import predict
import setup as lite

''' Converts coordinates from AZ, EL to HA, DEC '''
def AZELtoHADEC(AZEL):
    a = AZEL[1]
    z = 90 - a
    A = AZEL[0]
    phi = lite.refPos[0]
    # Python math requires radian values
    zRad = math.radians(z)
    ARad = math.radians(A)
    phiRad = math.radians(phi)
    dec = math.asin(math.cos(zRad) * math.sin(phiRad)
                    + math.sin(zRad) * math.cos(phiRad) * math.cos(ARad))
    ha = math.acos(math.cos(zRad) / (math.cos(dec) * math.cos(phiRad))
                   - math.tan(dec) * math.tan(phiRad))
    ha = math.degrees(ha) / 15.0
    dec = math.degrees(dec)
    if AZEL[0] > 0 and AZEL[0] < 180:
        ha *= -1

    return [ha, dec]

''' Get latitude, longitude, altitude, and time from APRS '''
def getAprsPos():
    url = "https://api.aprs.fi/api/get?name=" + lite.callsign + \
          "&what=loc&apikey=" + lite.aprsKey + "&format=xml"
    with urllib.request.urlopen(url) as f:
        text = f.readline()
        # This must be called twice
        text = f.readline()
        if text.find(b'<found>1'):
            outline = text.decode("utf-8")
            outline = outline.replace("<"," ").replace(">"," ")
            line = outline.split()

            lat = lng = alt = time = None
            i = 0
            while i < len(line):
                if line[i] == 'time' and not time:
                    i += 1
                    time = float(line[i])

                elif line[i] == 'lat' and not lat:
                    i += 1
                    lat = float(line[i])

                elif line[i] == 'lng' and not lng:
                    i += 1
                    lng = float(line[i])

                elif line[i] == 'altitude' and not alt:
                    i += 1
                    alt = float(line[i])
                i += 1

        # If callsign data not found
        if not (lat and lng and alt and time):
            lat = lng = alt = time = -404
    return [lat, lng, alt, time]

''' Check if data from APRS has updated '''
def checkUpdate(pos):
    # Return False if no update has occurred
    if lite.n > 0:
        if np.array_equal(pos, lite.log[lite.n - 1]["pos"]):
            return False
        else:
            return True
    else:
        return True

''' Pull data from APRS & perform calculations '''
def repeat():
    data = {}
    # Get current position
    entry = getAprsPos()
    data["pos"] = entry[0:3]
    data["aprsTime"] = entry[3]
    data["userTime"] = datetime.datetime.now()
    balloonPos = [entry[0], entry[1], entry[2]]

    # Get predicted position
    predPos = predict.predict(balloonPos)
    data["predPos"] = predPos
    source = "aprs"

    # Check if update has occured
    if len(lite.log) > 1:
        if not checkUpdate(entry[0:3]):
            source = "pred"
            lite.noUpdate += 1
        else:
            lite.noUpdate = 0
    data["source"] = source

    # Coordinate conversions
    az, el, range = pm.geodetic2aer(predPos[0], predPos[1], predPos[2],
                                    lite.refPos[0], lite.refPos[1], lite.refPos[2])
    predHADEC = AZELtoHADEC([az, el, range])

    # Add in offset
    predHADEC[0] += lite.offsetHA
    predHADEC[1] += lite.offsetDEC
    # Print HA, DEC
    print("--------------------------------------------\n"
          "   HA: " + str(round(predHADEC[0], 4)) + " deg\n"
          "  DEC: " + str(round(predHADEC[1], 4)) + " deg")
    data["azel"] = [az, el, range]
    data["hadec"] = predHADEC

    time.sleep(1)
    # String command sent to telescope
    strCmd = "#12;"
    # Minimum elevation for telescope movement is 16 deg
    if el >= 16 and not lite.pause and predHADEC != [-1, -1]:
        strCmd = "#33," + str(predHADEC[0]) + "," + str(predHADEC[1]) + ";"
    data["command"] = strCmd
    print(">> " + strCmd + "\n")

    # Data not up to date if callsign not found
    if lite.noUpdate == 0 and entry != [-404, -404, -404, -404]:
        print("Data is up to date")
    else:
        print("Data is not up to date\n"
              "Calls since last update: " + str(lite.noUpdate) + "\n")

    if lite.mode == "actual":
        lite.sock.send(bytes(strCmd, 'utf-8'))

    lite.log.append(data)
    time.sleep(1)

''' Specify mode to run in main() '''
def setMode():
    print("LITE has two modes for tracking")
    while True:
        mode = input("Run as 'TEST' or 'ACTUAL'?\n")

        ## TEST ##
        if mode.lower() == "test":
            confirm = input("Are you sure you want to begin running TEST?\n"
                            "Type 'yes' to confirm, anything else to re-enter\n")
            if confirm.lower() == "yes":
                print("Running TEST ....\n")
                break

        ## ACTUAL ##
        elif mode.lower() == "actual":
            confirm = input("Telescope will begin moving\n"
                            "Are you sure you want to begin running ACTUAL?\n"
                            "Type 'yes' to confirm, anything else to re-enter\n")
            if confirm.lower() == "yes":
                ## TCP/IP ##
                print("Connecting to telescope ....\n")
                lite.TCP_IP = lite.setVar("IP address")
                lite.TCP_PORT = int(lite.setVar("port number"))
                lite.sock = socket.socket
                lite.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                lite.sock.connect((lite.TCP_IP, lite.TCP_PORT))
                print("Connection established ....\n")
                lite.mode = "actual"
                print("Running ACTUAL ....\n")
                break

        else:
            print("Invalid mode\n")