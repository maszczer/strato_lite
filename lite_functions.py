import datetime, math
import pymap3d as pm
import time, urllib.request
import lite_config as c
import lite_predict as predict

# Converts coordinates from AZ, EL to HA, DEC
def AZELtoHADEC(AZEL):
    a = AZEL[1]
    z = 90 - a
    A = AZEL[0]
    phi = c.refPos[0]
    #convert to radians because python
    zRad = math.radians(z)
    ARad = math.radians(A)
    phiRad = math.radians(phi)
    dec = math.asin(math.cos(zRad) * math.sin(phiRad) + math.sin(zRad) * math.cos(phiRad) * math.cos(ARad))
    ha = math.acos(math.cos(zRad) / (math.cos(dec) * math.cos(phiRad)) - math.tan(dec) * math.tan(phiRad))

    ha = math.degrees(ha) / 15.0
    dec = math.degrees(dec)
    if ((AZEL[0] > 0) & (AZEL[0] < 180)):
        ha *= -1

    return [ha, dec]

# Get latitude, longitude, altitude, and time from APRS
# Use an automated process to call this function
def getCoord():
    url = "https://api.aprs.fi/api/get?name=" + c.callsign + "&what=loc&apikey=" + c.aprsKey + "&format=xml"
    with urllib.request.urlopen(url) as f:
        fak = f.readline()
        fak = f.readline() # This must be called twice
        if (fak.find(b'<found>1')):
            outline = fak.decode("utf-8")
            outline = outline.replace("<"," ")
            outline = outline.replace(">"," ")
            line = outline.split()

            lat = 0; lng = 0
            alt = 0; time = 0

            latFound = 0; lngFound = 0
            altFound = 0; timeFound = 0

            i = 0
            while (i < len(line)):
                if (line[i] == 'time' and timeFound == 0):
                    i += 1
                    time = float(line[i])
                    timeFound = 1

                elif (line[i] == 'lat' and latFound == 0):
                    i += 1
                    lat = float(line[i])
                    latFound = 1

                elif (line[i] == 'lng' and lngFound == 0):
                    i += 1
                    lng = float(line[i])
                    lngFound = 1

                elif (line[i] == 'altitude' and altFound == 0):
                    i += 1
                    alt = float(line[i])
                    altFound = 1

                i += 1

    return [lat, lng, alt, time]

# Check if data from APRS has updated
# Return 0 if no update has occured
# Return 1 if updated has occured
def checkUpdate():
    if (c.n > 0):
        if ((c.log[c.n][0] == c.log[c.n-1][0])
            & (c.log[c.n][1] == c.log[c.n-1][1])
            & (c.log[c.n][2] == c.log[c.n-1][2])):
            c.noUpdate += 1
            return 0
        else:
            c.noUpdate = 0
            return 1
    else:
        c.noUpdate = 0
        return 1

# Repeat these functions within loop
def repeat():
    entry = []
    entry = getCoord()
    entry.append(datetime.datetime.now())
    c.log.append(entry)
    balloonPos = [entry[0], entry[1], entry[2]]
    predPos = predict.predict(balloonPos)
    source = "aprs"

    c.predLog.append(predPos)
    if (len(c.log) - 1 > 0):
        if (checkUpdate() == 0):
            balloonPos = [c.predLog[len(c.log) - 2][0], c.predLog[len(c.log) - 2][1], c.predLog[len(c.log) - 2][2]]
            c.predLog[len(c.log) - 1] = predict.predict(balloonPos)

            c.noUpdate += 1
            source = "pred"
        else:
            c.noUpdate = 0

    # data is stored in in log as a list
    # [lat, lng, alt, time, timestamp, az, el, range, ha, dec, strOut]
    az, el, range = pm.geodetic2aer(predPos[0], predPos[1], predPos[2], c.refPos[0], c.refPos[1], c.refPos[2])
    predOut = AZELtoHADEC([az, el, range])

    # add in offset
    predOut[0] += c.offsetHA
    predOut[1] += c.offsetDEC

    print("   HA: " + str(predOut[0]) + " deg")
    print("  DEC: " + str(predOut[1]) + " deg")

    extraData = [az, el, range]
    c.log[len(c.log) - 1].extend(extraData)
    c.log[len(c.log) - 1].extend(predOut)

    strOut = ("#33," + str(predOut[0]) + "," + str(predOut[1]) + ";\n")
    time.sleep(1)
    # minimum elevation for telescope movement is 16 deg
    if ((c.pause == 0) & (el > 16)):
        strOut = ("#12;\n")

    c.log[len(c.log) - 1].append(strOut)
    print(">> " + strOut)
    if (c.mode == "actual"):
        c.sock.send(bytes(strOut, 'utf-8'))

    c.log[len(c.log) - 1].append(source)
    time.sleep(1)