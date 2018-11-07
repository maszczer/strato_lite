import csv, datetime, time
import functions as fcn
import setup as lite
import threading

# autoThread sends commands to the telescope while live == 1
class autoThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        # Output log to csv
        filename = 'tracking_' + lite.mode + '_' + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.csv'
        with open(filename, 'w') as myfile:
            writer = csv.writer(myfile, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_ALL)
            writer.writerow(["lat (deg)", "lng (deg)", "alt (m)", "APRS timestamp","user timestamp", "az (deg)",
                             "el (deg)", "range (m)", "ha (deg)", "dec (deg)", "command (strOut)",
                             "predLat (deg)", "predLng (deg)", "predAlt (m)", "source"])

            while (lite.live == 1):
                fcn.repeat()
                # Send new log[] data to .csv
                data = []
                with lite.log[lite.n] as liteData:
                    data.extend(liteData["pos"])
                    data.append(liteData["aprsTime"])
                    data.append(liteData["userTime"])
                    data.extend(liteData["azel"])
                    data.extend(liteData["hadec"])
                    data.append(liteData["command"])
                    data.extend(liteData["predPos"])
                    data.append(liteData["source"])
                writer.writerow(data)
                # Flush buffer, force write to .csv
                myfile.flush()
                lite.printed = 1
                lite.n += 1
                time.sleep(lite.timer)

# userThread allows for commands during flight
class userThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while (lite.live == 1):
            command = input("(Type 'h' or 'help' to list commands)\n")
            # Help
            # List commands
            if ((command.lower() == 'h') | (command.lower() == "help")):
                print("'d' or 'data' display most recent data\n"
                      "'p' or 'pause' pause telescope movement (toggles on/off)\n"
                      "'o' or 'offset' change offset to HA, DEC\n"
                      "'r' or 'reset' orient telescope to default position\n"
                      "'s' or 'status' display flight setup info\n"
                      "'q' or 'quit' quit program\n")

            # Status
            # Print flight setup info
            elif ((command.lower() == 's') | (command.lower() == "status")):
                print("APRS key: " + lite.aprsKey +
                      "Output mode: " + lite.mode +
                      "Update occurs every " + str(lite.timer + 2) + " sec" +
                      "Telescope coordinates : [" + str(lite.refPos[0]) + ", "+
                      str(lite.refPos[1]) + ", " + str(lite.refPos[2]) + "]"
                      "TCP_IP: " + lite.TCP_IP +
                      "TCP_PORT: " + lite.TCP_PORT + "\n" +
                      "Program has been running for " +
                      str(round(lite.n * (lite.timer + 2) / 60), 4) + " min")#buggy

            # Data
            # Print most recent data
            # Will be more detailed than standard output
            elif ((command.lower() == 'd') | (command.lower() == "data")):
                if (lite.printed == 1):
                    val = 0
                    if (lite.n > 0):
                        val = lite.n - 1
                        with lite.log[val] as liteData:
                            print("Using " + liteData["source"] + " data:\n" +
                                  "  LAT: " + str(liteData["pos"][0]) + " deg\n" +
                                  "  LNG: " + str(liteData["pos"][1]) + " deg\n" +
                                  "  ALT: " + str(liteData["pos"][2]) + " m\n" +
                                  " TIME: " + str(liteData["aprsTime"]) + "\n" +
                                  "   AZ: " + str(liteData["azel"][0]) + " deg\n" +
                                  "   EL: " + str(liteData["azel"][1]) + " deg\n" +
                                  "RANGE: " + str(liteData["azel"][2]) + " m\n" +
                                  "   HA: " + str(liteData["hadec"][0]) + " deg" +
                                  " w/ offset " + str(lite.offsetHA) + "\n"
                                  "  DEC: " + str(liteData["hadec"][1]) + " deg" +
                                  " w/ offset " + str(lite.offsetDEC) + "\n" +
                                  "Predicted\n" +
                                  "  LAT: " + str(liteData["predPos"][0]) + " deg\n" +
                                  "  LNG: " + str(liteData["predPos"][1]) + " deg\n" +
                                  "  ALT: " + str(liteData["predPos"][2]) + " m\n" +
                                  ">> " + liteData["command"])
                    if (lite.noUpdate == 0):
                        print("Data is up to date")
                    else:
                        print("Calls since last update: " + str(lite.noUpdate))
                    print(str(lite.log[val]["userTime"]))
                    if (lite.pause == 1):
                        print("Telescope movement is paused\n")
                    else:
                        print("Telescope movement is active\n")
                else:
                    print("Loading data, please wait and try again\n")

            # Offset
            # Change offset for HA, DEC
            elif ((command.lower() == 'o') | (command.lower() == "offset")):
                print(" HA offset = " + str(lite.offsetHA) +
                      "DEC offset = " + str(lite.offsetDEC))
                ha = input("> Enter new HA offset\n")
                dec = input("> Enter new DEC offset\n")
                if((lite.checkNum(ha) == 1) & (lite.checkNum(dec))):
                    newHA = float(ha)
                    newDEC = float(dec)
                    print("New (HA, DEC) offset will be (" + ha + ", " + dec + ")")
                    val = input("Are you sure you want to change HA, DEC offset?\n"
                                "Type 'yes' to change, anything else to cancel\n")
                    if (val.lower() == "yes"):
                        lite.offsetHA = newHA
                        lite.offsetDEC = newDEC
                        print("Offset changed to (" + str(lite.offsetHA) + ", " + str(lite.offsetDEC) + ")\n")
                    else:
                        print("Offset unchanged, still (" + str(lite.offsetHA) + ", " + str(lite.offsetDEC) + ")\n")
                else:
                    print("HA & DEC must be numbers\n"
                          "Offset unchanged, still (" + str(lite.offsetHA) + ", " + str(lite.offsetDEC) + ")\n")

            # Pause
            # Pause/resume telescope movement, while maintaining tracking
            elif ((command.lower() == 'p') | (command.lower() == "pause")):
                if (lite.pause == 0):
                    lite.pause = 1
                    print("Telescope movement is paused\n")
                else:
                    lite.pause = 0
                    print("Resuming telescope movement ....\n")

            # Quit
            # End program prematurely
            elif ((command.lower() == 'q') | (command.lower() == "quit")):
                val = input("Are you sure you want to quit?\n"
                            "Type 'yes' to quit, anything else to cancel\n")
                if (val.lower() == "yes"):
                    print("Quitting ....")
                    lite.live = 0
                    if (lite.mode == "actual"):
                        lite.sock.close()
                    exit(0)
                else :
                    print("Resuming tracking ....\n")

            # Reset
            # Send telescope to HA 3.66 and DEC -6.8
            elif ((command.lower() == 'r') | (command.lower() == "reset")):
                val = input("Are you sure you want to reset orientation to the default position?\n"
                            "Type 'yes' to move, anything else to cancel\n")
                if (val.lower() == "yes"):
                    defOut = ("#33,3.66,-6.8;")
                    print(">> " + defOut)
                    if (lite.mode == "actual"):
                        lite.sock.send(bytes(defOut, 'utf-8'))
                    defOut = ("#12;")
                    print(">> " + defOut + "\n")
                    if (lite.mode == "actual"):
                        lite.sock.send(bytes(defOut, 'utf-8'))
                else:
                    print("Resuming tracking ....\n")

            # No other valid commands
            else:
                print("Invalid command\n")