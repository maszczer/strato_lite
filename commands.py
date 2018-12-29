"""
Functions for each user command
These are called by userThread() in threads.py
"""
import queue
import setup as lite

''' List available user commands '''
def listCmds():
    print("-- HELP --\n"
          "'d' or 'data' display most recent data\n"
          "'p' or 'pause' pause telescope movement (toggles on/off)\n"
          "'o' or 'offset' change offset to HA, DEC\n"
          "'r' or 'reset' orient telescope to default position\n"
          "'s' or 'status' display flight setup info\n"
          "'q' or 'quit' quit program\n")

''' Print flight setup info '''
def status():
    print("-- STATUS --\n"
          "APRS key: " + lite.aprsKey + "\n" +
          "Output mode: " + lite.mode + "\n" +
          "Telescope coordinates : [" + str(lite.refPos[0]) + ", " +
          str(lite.refPos[1]) + ", " + str(lite.refPos[2]) + "]\n"
          "TCP_IP: " + lite.TCP_IP + "\n" +
          "TCP_PORT: " + str(lite.TCP_PORT) + "\n" +
          "Program has been running for " +
          str(round(lite.n * 10 / 60, 4)) + " min")  # buggy

''' Returns string for printing latitude, longitude, altitude '''
def printPos(pos):
    data = "  LAT: " + str(pos[0]) + " deg\n" + \
           "  LNG: " + str(pos[1]) + " deg\n" + \
           "  ALT: " + str(pos[2]) + " m\n"
    return data

''' Print most recent data, more detailed than standard output '''
def data():
    if lite.printed:
        i = 0
        if lite.n > 0:
            i = lite.n - 1
            print("-- DATA --\n"
                  "Using " + lite.log[i]["source"] + " data:\n" +
                  printPos(lite.log[i]["pos"]) +
                  " TIME: " + str(lite.log[i]["aprsTime"]) + "\n" +
                  printPos(lite.log[i]["azel"]) +
                  "   HA: " + str(lite.log[i]["hadec"][0]) + " deg" +
                  " w/ offset " + str(lite.offsetHA) + "\n"
                  "  DEC: " + str(lite.log[i]["hadec"][1]) + " deg" +
                  " w/ offset " + str(lite.offsetDEC) + "\n" +
                  "Predicted:\n" + printPos(lite.log[i]["predPos"]) +
                  ">> " + lite.log[i]["command"])

        if lite.lastGrndUpdate == 0:
            print("Ground Station data is up to date")
        else:
            print("Calls since last Ground Station update: " + str(lite.lastGrndUpdate))

        if lite.lastAprsUpdate == 0:
            print("APRS data is up to date")
        else:
            print("Calls since last APRS update: " + str(lite.lastAprsUpdate))

        print(str(lite.log[i]["isotime"]))

        if lite.pause:
            print("Telescope movement is paused\n")
        else:
            print("Telescope movement is active\n")

    else:
        print("Loading data, please wait and try again\n")

''' Change offset for HA, DEC '''
def offset():
    print("-- OFFSET --\n"
          " HA offset = " + str(lite.offsetHA) +
          "DEC offset = " + str(lite.offsetDEC))
    ha = input("> Enter new HA offset\n")
    dec = input("> Enter new DEC offset\n")
    if lite.checkNum(ha) and lite.checkNum(dec):
        newHA = float(ha)
        newDEC = float(dec)
        print("New (HA, DEC) offset will be (" + ha + ", " + dec + ")")
        confirm = input("Are you sure you want to change HA, DEC offset?\n"
                    "Type 'yes' to change, anything else to cancel\n")

        if confirm.lower() == "yes":
            lite.offsetHA = newHA
            lite.offsetDEC = newDEC
            print("Offset changed to (" + str(lite.offsetHA) +
                  ", " + str(lite.offsetDEC) + ")\n")
        else:
            print("Offset unchanged, still (" + str(lite.offsetHA) +
                  ", " + str(lite.offsetDEC) + ")\n")

    else:
        print("HA & DEC must be numbers\n"
              "Offset unchanged, still (" + str(lite.offsetHA) + ", " +
              str(lite.offsetDEC) + ")\n")

''' Pause/resume telescope movement '''
def pause():
    print("-- PAUSE --\n")
    if not lite.pause:
        lite.pause = True
        print("Telescope movement is paused\n")
    else:
        lite.pause = False
        print("Resuming telescope movement ....\n")

''' End program '''
def shutdown():
    confirm = input("-- QUIT --\n"
                    "Are you sure you want to quit?\n"
                    "Type 'yes' to quit, anything else to cancel\n")
    if confirm.lower() == "yes":
        print("Quitting ....")
        lite.live = False
        if lite.mode == "actual":
            lite.sock.close()
        exit(0)
    else:
        print("Resuming tracking ....\n")

''' Send telescope to HA 3.66 and DEC -6.8 '''
def reset():
    confirm = input("-- RESET --\n"
                    "Are you sure you want to reset orientation to the default position?\n"
                    "Type 'yes' to move, anything else to cancel\n")
    if confirm.lower() == "yes":
        strCmd = ("#33,3.66,-6.8;")
        print(">> " + strCmd)

        if lite.mode == "actual":
            lite.sock.send(bytes(strCmd, 'utf-8'))
        strCmd = ("#12;")
        print(">> " + strCmd + "\n")

        if lite.mode == "actual":
            lite.sock.send(bytes(strCmd, 'utf-8'))

    else:
        print("Resuming tracking ....\n")