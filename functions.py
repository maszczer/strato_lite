import datetime, math
import pymap3d as pm
import time, urllib.request
import predict
import setup as lite

# Converts coordinates from AZ, EL to HA, DEC
def AZELtoHADEC(AZEL):
    a = AZEL[1]
    z = 90 - a
    A = AZEL[0]
    phi = lite.refPos[0]
    #convert to radians because python
    zRad = math.radians(z)
    ARad = math.radians(A)
    phiRad = math.radians(phi)
    dec = math.asin(math.cos(zRad) * math.sin(phiRad)+ math.sin(zRad)
                    * math.cos(phiRad) * math.cos(ARad))
    ha = math.acos(math.cos(zRad) / (math.cos(dec) * math.cos(phiRad))
                   - math.tan(dec) * math.tan(phiRad))
    ha = math.degrees(ha) / 15.0
    dec = math.degrees(dec)
    if ((AZEL[0] > 0) & (AZEL[0] < 180)):
        ha *= -1

    return [ha, dec]

# Get latitude, longitude, altitude, and time from APRS
# Use an automated process to call this function
def getCoord():
    url = "https://api.aprs.fi/api/get?name=" + lite.callsign + \
          "&what=loc&apikey=" + lite.aprsKey + "&format=xml"
    with urllib.request.urlopen(url) as f:
        fak = f.readline()
        # This must be called twice
        fak = f.readline()
        if (fak.find(b'<found>1')):
            outline = fak.decode("utf-8")
            outline = outline.replace("<"," ")
            outline = outline.replace(">"," ")
            line = outline.split()

            lat = None; lng = None
            alt = None; time = None

            i = 0
            while (i < len(line)):
                if (line[i] == 'time' and not time):
                    i += 1
                    time = float(line[i])

                elif (line[i] == 'lat' and not lat):
                    i += 1
                    lat = float(line[i])

                elif (line[i] == 'lng' and not lng):
                    i += 1
                    lng = float(line[i])

                elif (line[i] == 'altitude' and not alt):
                    i += 1
                    alt = float(line[i])

                i += 1

    return [lat, lng, alt, time]

# Check if data from APRS has updated
'''
Return 0 if no update has occured
Return 1 if updated has occured
'''
def checkUpdate():
    if (n > 0):
        if ((lite.log[n]["pos"][0] == lite.log[n-1]["pos"][0])
            & (lite.log[n]["pos"][1] == lite.log[n-1]["pos"][1])
            & (lite.log[n]["pos"][2] == lite.log[n-1]["pos"][2])):
            return 0
        else:
            return 1
    else:
        return 1

# Repeat these functions within loop
def repeat():
    data = {}
    entry = getCoord()
    data["pos"] = entry[0:3]
    data["aprsTime"] = entry[3]
    data["userTime"] = datetime.datetime.now()
    balloonPos = [entry[0], entry[1], entry[2]]

    predPos = predict.predict(balloonPos)
    data["predPos"] = predPos
    source = "aprs"

    # Check if update has occured
    if (len(lite.log) - 1 > 0):
        if (checkUpdate() == 0):
            source = "pred"; lite.noUpdate += 1
        else:
            lite.noUpdate = 0
    data["source"] = source

    # Coordinate conversions
    az, el, range = pm.geodetic2aer(predPos[0], predPos[1], predPos[2],
                                    lite.refPos[0], lite.refPos[1], lite.refPos[2])
    predOut = AZELtoHADEC([az, el, range])

    # add in offset
    predOut[0] += lite.offsetHA
    predOut[1] += lite.offsetDEC

    print("--------------------------------------------\n"
          "   HA: " + str(round(predOut[0], 4)) + " deg\n"
          "  DEC: " + str(round(predOut[1], 4)) + " deg")

    data["azel"] = [az, el, range]
    data["hadec"] = [predOut]

    # String command sent to telescope
    strOut = ("#33," + str(predOut[0]) + "," + str(predOut[1]) + ";\n")
    time.sleep(1)
    # minimum elevation for telescope movement is 16 deg
    if ((lite.pause == 0) & (el > 16)):
        strOut = ("#12;\n")
    data["command"] = strOut
    print(">> " + strOut)

    if (lite.noUpdate == 0):
        print("Data is up to date")
    else:
        print("Calls since last update: " + str(lite.noUpdate) + "\n")
    if (lite.mode == "actual"):
        lite.sock.send(bytes(strOut, 'utf-8'))

    lite.log.append(data)
    time.sleep(1)