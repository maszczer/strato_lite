import csv
import lite_functions as fcn
import threading, time
import lite_config as c

# autoThread sends commands to the telescope while live == 1
class autoThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        # output log to csv
        with open('tracking_TEST_data.csv', 'w') as myfile:
            writer = csv.writer(myfile, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_ALL)
            writer.writerow(["lat (deg)", "lng (deg)", "alt (m)", "time", "timestamp", "az (deg)", "el (deg)", "range (m)", "ha (deg)", "dec (deg)", "command (strOut)"])

            while (c.live == 1):
                #print(str(n));
                fcn.repeat()
                writer.writerow(c.log[c.n]) # send new log[] data to .csv
                myfile.flush() # flushes buffer, forces write to .csv
                c.printed = 1
                c.n += 1
                time.sleep(c.timer)

# userThread allows for commands during flight
class userThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while (c.live == 1):
            command = input("(Type 'h' or 'help' to list commands)\n\n")
            # Help
            # List commands
            if ((command.lower() == 'h') | (command.lower() == "help")):
                print("'d' or 'data' display most recent data\n'p' or 'pause' pause telescope movement (toggles on/off)\n'o' or 'offset' change offset to HA, DEC\n")
                print("'r' or 'reset' orient telescope to default position\n's' or 'status' display flight setup info\n'q' quit program\n")

            # Status
            # Print flight setup info
            elif ((command.lower() == 's') | (command.lower() == "status")):
                print("APRS key: " + c.aprsKey)
                print("Output mode: " + c.mode)
                print("Telescope coordinates : [" + str(c.refPos[0]) + ", " + str(c.refPos[1]) + ", " + str(c.refPos[2]) + "]")
                print("TCP_IP: " + c.TCP_IP)
                print("TCP_PORT: " + c.TCP_PORT + "\n")

            # Data
            # Print most recent data
            # Will be more detailed than standard output
            elif ((command.lower() == 'd') | (command.lower() == "data")):
                if (c.printed == 1):
                    val = 0
                    if (c.n > 0):
                        val = c.n - 1
                    if (c.noUpdate == 0):
                        print("Data is up to date")
                    else:
                        print("Calls since last update: " + str(c.noUpdate))
                    print("  LAT: " + str(c.log[val][0]) + " deg")
                    print("  LNG: " + str(c.log[val][1]) + " deg")
                    print("  ALT: " + str(c.log[val][2]) + " deg")
                    print(" TIME: " + str(c.log[val][3]))
                    print("   AZ: " + str(c.log[val][5]) + " deg")
                    print("   EL: " + str(c.log[val][6]) + " deg")
                    print("RANGE: " + str(c.log[val][7]) + " m")
                    print("   HA: " + str(c.log[val][8]) + " deg & offset " + str(c.offsetHA))
                    print("  DEC: " + str(c.log[val][9]) + " deg & offset " + str(c.offsetDEC))
                    print(">> " + str(c.log[val][10]))
                    print(str(c.log[val][4]))
                    if (c.pause == 1):
                        print("Telescope movement is paused\n")
                    else:
                        print("Telescope movement is active\n")
                else:
                    print("Loading data, please wait and try again\n")

            # Offset
            # Change offset for HA, DEC
            elif ((command.lower() == 'o') | (command.lower() == "offset")):
                print(" HA offset = " + str(c.offsetHA))
                print("DEC offset = " + str(c.offsetDEC))
                val = input("> Enter new HA offset")
                newHA = float(val)
                val = input("> Enter new DEC offset")
                newDEC = float(val)
                print("New (HA, DEC) offset will be (" + str(newHA) + ", " + str(newDEC) + ")")
                val = input("Are you sure you want to change HA, DEC offset?\nType 'yes' to change, anything else to cancel\n")
                if (val.lower() == "yes"):
                    c.offsetHA = newHA
                    c.offsetDEC = newDEC
                    print("Offset changed to (" + str(c.offsetHA) + ", " + str(c.offsetDEC) + ")\n")
                else:
                    print("Offset unchanged, still (" + str(c.offsetHA) + ", " + str(c.offsetDEC) + ")\n")

            # Pause
            # Pause/resume telescope movement, while maintaining tracking
            elif ((command.lower() == 'p') | (command.lower() == "pause")):
                if (c.pause == 0):
                    c.pause = 1
                    print("Telescope movement is paused\n")
                else:
                    c.pause = 0
                    print("Resuming telescope movement ....\n")

            # Quit
            # End program prematurely
            elif ((command.lower() == 'q') | (command.lower() == "quit")):
                val = input("Are you sure you want to quit?\nType 'yes' to quit, anything else to cancel\n")
                if (val.lower() == "yes"):
                    print("Quitting ....")
                    c.live = 0
                    if (c.mode == "actual"):
                        c.sock.close()
                    exit(0)
                else :
                    print("Resuming tracking ....\n")

            # Reset
            # Send telescope to HA 3.66 and DEC -6.8
            elif ((command.lower() == 'r') | (command.lower() == "reset")):
                val = input("Are you sure you want to reset orientation to the default position?\nType 'yes' to move, anything else to cancel\n");
                if (val.lower() == "yes"):
                    defOut = ("#33,3.66,-6.8;")
                    print(">> " + defOut)
                    if (c.mode == "actual"):
                        c.sock.send(bytes(defOut, 'utf-8'))
                    defOut = ("#12;")
                    print(">> " + defOut + "\n")
                    if (c.mode == "actual"):
                        c.sock.send(bytes(defOut, 'utf-8'))
                else:
                    print("Resuming tracking ....\n")

            # No other valid commands
            else:
                print("Invalid command\n")