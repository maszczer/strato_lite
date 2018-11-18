"""
Functions for each user command
These are called by userThread() in threads.py
"""
import setup as lite

''' List available user commands '''
def listCmds():
    print("'d' or 'data' display most recent data\n"
          "'p' or 'pause' pause telescope movement (toggles on/off)\n"
          "'o' or 'offset' change offset to HA, DEC\n"
          "'r' or 'reset' orient telescope to default position\n"
          "'s' or 'status' display flight setup info\n"
          "'q' or 'quit' quit program\n")

''' Print flight setup info '''
def status():
    print("APRS key: " + lite.aprsKey + "\n" +
          "Output mode: " + lite.mode + "\n" +
          "Update occurs every " + str(lite.timer + 2) + " sec" + "\n" +
          "Telescope coordinates : [" + str(lite.refPos[0]) + ", " +
          str(lite.refPos[1]) + ", " + str(lite.refPos[2]) + "]\n"
          "TCP_IP: " + lite.TCP_IP + "\n" +
          "TCP_PORT: " + lite.TCP_PORT + "\n" +
          "Program has been running for " +
          str(round(lite.n * (lite.timer + 2) / 60, 4)) + " min")  # buggy

''' Print most recent data, more detailed than standard output '''
def data():
    if lite.printed:
        i = 0
        if lite.n > 0:
            i = lite.n - 1
            print("Using " + lite.log[i]["source"] + " data:\n" +
                  "  LAT: " + str(lite.log[i]["pos"][0]) + " deg\n" +
                  "  LNG: " + str(lite.log[i]["pos"][1]) + " deg\n" +
                  "  ALT: " + str(lite.log[i]["pos"][2]) + " m\n" +
                  " TIME: " + str(lite.log[i]["aprsTime"]) + "\n" +
                  "   AZ: " + str(lite.log[i]["azel"][0]) + " deg\n" +
                  "   EL: " + str(lite.log[i]["azel"][1]) + " deg\n" +
                  "RANGE: " + str(lite.log[i]["azel"][2]) + " m\n" +
                  "   HA: " + str(lite.log[i]["hadec"][0]) + " deg" +
                  " w/ offset " + str(lite.offsetHA) + "\n"
                  "  DEC: " + str(lite.log[i]["hadec"][1]) + " deg" +
                  " w/ offset " + str(lite.offsetDEC) + "\n" +
                  "Predicted:\n" +
                  "  LAT: " + str(lite.log[i]["predPos"][0]) + " deg\n" +
                  "  LNG: " + str(lite.log[i]["predPos"][1]) + " deg\n" +
                  "  ALT: " + str(lite.log[i]["predPos"][2]) + " m\n" +
                  ">> " + lite.log[i]["command"])

        if lite.noUpdate == 0:
            print("Data is up to date")
        else:
            print("Calls since last update: " + str(lite.noUpdate))

        print(str(lite.log[i]["userTime"]))

        if lite.pause:
            print("Telescope movement is paused\n")
        else:
            print("Telescope movement is active\n")

    else:
        print("Loading data, please wait and try again\n")

''' Change offset for HA, DEC '''
def offset():
    print(" HA offset = " + str(lite.offsetHA) +
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
            print("Offset changed to (" + str(lite.offsetHA) + ", " + str(lite.offsetDEC) + ")\n")
        else:
            print("Offset unchanged, still (" + str(lite.offsetHA) + ", " + str(lite.offsetDEC) + ")\n")

    else:
        print("HA & DEC must be numbers\n"
              "Offset unchanged, still (" + str(lite.offsetHA) + ", " + str(lite.offsetDEC) + ")\n")

''' Pause/resume telescope movement '''
def pause():
    if not lite.pause:
        lite.pause = True
        print("Telescope movement is paused")
    else:
        lite.pause = False
        print("Resuming telescope movement ....\n")

''' End program '''
def shutdown():
    confirm = input("Are you sure you want to quit?\n"
                "Type 'yes' to quit, anything else to cancel\n")
    if confirm.lower() == "yes":
        print("Quitting ....")
        lite.live = 0
        if lite.mode == "actual":
            lite.sock.close()
        exit(0)
    else:
        print("Resuming tracking ....\n")

''' Send telescope to HA 3.66 and DEC -6.8 '''
def reset():
    confirm = input("Are you sure you want to reset orientation to the default position?\n"
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