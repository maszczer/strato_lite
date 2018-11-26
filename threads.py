"""
Repeat these functions until the quit command is entered
"""
import csv, datetime, time
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
            "APRS timestamp",
            "user timestamp",
            "az (deg)",
            "el (deg)",
            "range (m)",
            "ha (deg)",
            "dec (deg)",
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
                "aprsTime",
                "userTime",
                "azel",
                "hadec",
                "predPos",
                "command",
                "source"
            ]
            for datum in logData:
                try:
                    data.extend(lite.log[lite.n][datum])
                except TypeError:
                    data.append(lite.log[lite.n][datum])
            writer.writerow(data)
            # Flush buffer, force write to .csv
            myfile.flush()
            lite.n += 1
            lite.printed = True
            time.sleep(lite.timer)

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
