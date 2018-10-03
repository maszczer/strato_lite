import lite_threading as thread
import lite_config as c
import socket

def main():
    # Select a mode to run - TEST or ACTUAL
    selected = 0
    print("LITE has two modes for tracking")
    while (selected == 0):
        strIn = input("Run as 'TEST' or 'ACTUAL'?\n")
        # TEST
        if (strIn.lower() == "test"):
            selected = 1
            print("Running TEST ....\n")

        # ACTUAL
        elif (strIn.lower() == "actual"):
            strIn = input("Telescope will begin moving\nAre you sure you want to begin ACTUAL?\n")
            if (strIn.lower == "yes"):
                ## TCP/IP ##
                print("Connecting to telescope ....\n")
                n = 0; strIn = "null"
                while (n == 0):
                    strIn = input("> Enter IP address")
                    print("IP address : " + strIn)
                    if (input("Is this correct?\nType 'yes' to confirm, anything else to re-enter\n") == "yes"):
                        n = 1
                TCP_IP = strIn
                c.TCP_IP = TCP_IP

                n = 0; strIn = "null"
                while (n == 0):
                    strIn = input("> Enter port number")
                    print("Port number : " + strIn)
                    if (input("Is this correct?\nType 'yes' to confirm, anything else to re-enter\n") == "yes"):
                        n = 1
                TCP_PORT = strIn
                c.TCP_PORT = TCP_PORT
                TCP_PORT = float(TCP_PORT)

                c.sock = socket.socket
                c.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                c.sock.connect((TCP_IP, TCP_PORT))
                print("Connection established ....\n")
                c.mode = "actual"
                selected = 1
                print("Running ACTUAL ....\n")

            else:
                print("Not running ACTUAL ....\n")

        else:
            print("Invalid mode\n")

    threadA = thread.autoThread()
    threadB = thread.userThread()
    threadA.start()
    threadB.start()

if (__name__ == "__main__"):
    main()

'''
TODO
[x] Add offsets for HA, DEC
[x] Implement offset 'o' to change offset to HA, DEC
[x] set minimum elevation of 16 degrees instead of 18
[x] Change default 'd' to reset 'r' 
[x] Update recurring print for time, aprs data, predicted HA, DEC, any offset, time since last APRS update, etc
[x] Implement data 'd' to print more detailed info for most recent data
 * Still needs offset for HA, DEC, time since last APRS update
[ ] Print error from previous data

NOTE
 * If GPS data is pulled instead of APRS.fi, make sure format is compatible
 * data stored in log[lat, lng, alt, time, timestamp, az, el, range, ha, dec, strOut]
'''