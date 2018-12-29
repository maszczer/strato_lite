"""
Repeat these functions until the quit command is entered
"""
import csv, datetime, socket, time
import setup as lite
import commands as cmd
import functions as fcn

''' Pulls data from APRS, performs calculations, & outputs to .csv file '''
def autoThread():
    # Output log to csv
    filename = 'tracking_' + lite.mode + '_'\
               + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.csv'
    with open(filename, 'w') as myfile:
        writer = csv.writer(myfile, delimiter=',',
                            lineterminator='\n', quoting=csv.QUOTE_ALL)
        writer.writerow([
            "lat (deg)",
            "lng (deg)",
            "alt (m)",
            "az (deg)",
            "el (deg)",
            "range (m)",
            "ha (deg)",
            "dec (deg)",
            "utime",
            "isotime",
            "grndLat (deg)",
            "grndLng (deg)",
            "grndAlt (m)",
            "aprsLat (deg)",
            "aprsLng (deg)",
            "aprsAlt (m)",
            "predLat (deg)",
            "predLng (deg)",
            "predAlt (m)",
            "command",
            "source"
        ])

        while lite.live:
            fcn.repeat()
            # Send new log[] data to .csv
            data = []
            logData = [
                "pos",
                "azel",
                "hadec",
                "utime",
                "isotime",
                "grndPos",
                "aprsPos",
                "predPos",
                "command",
                "source"
            ]
            for datum in logData:
                # Ensure string values are not extended as char arrays
                if datum == "command" or datum == "source":
                    data.append(lite.log[lite.n][datum])
                else:
                    try:
                        data.extend(lite.log[lite.n][datum])
                    except TypeError:
                        data.append(lite.log[lite.n][datum])
            writer.writerow(data)
            # Flush buffer, force write to .csv
            myfile.flush()
            lite.n += 1
            lite.printed = True
            # Sleep for 8 sec, since 2 sec buffer in repeat()
            time.sleep(8)

''' Handles mid-flight user commands '''
def userThread():
    options = {
        "h": cmd.listCmds, "help": cmd.listCmds,
        "s": cmd.status, "status": cmd.status,
        "d": cmd.data, "data": cmd.data,
        "o": cmd.offset, "offset": cmd.offset,
        "p": cmd.pause, "pause": cmd.pause,
        "q": cmd.shutdown, "quit": cmd.shutdown,
        "r": cmd.reset, "reset": cmd.reset,
    }
    while lite.live:
        command = input("Type 'h' or 'help' to list commands\n")
        try:
            options[command]()
        except KeyError:
            print("Invalid command\n")

''' Listens for TCP packets from Ground Station on port 6000 '''
def grndThread():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 6000))
    sock.listen(5)
    client_sock = sock.accept()[0]
    while lite.live:
        data = client_sock.recv(1024)
        lite.grndPos = fcn.getGrndPos(data)
        time.sleep(10)
    sock.close()
