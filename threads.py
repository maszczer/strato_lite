import csv
import commands as cmd
import config as lite
import datetime
import functions as fcn
import loops
import time

def auto_thread_10_ground():
    ''' Update Ground Station data '''
    # This is a separate thread to maintain functionality in the event of errors
    loops.every_10_ground()
    time.sleep(10)

def auto_thread_10_else():
    ''' Update prediction data and write log data to .csv '''
    # Setup output file for flight-data
    filename = "lite_tracking_flight_data_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
    with open(filename, 'w') as file:
        writer = csv.writer(file, delimiter=',',
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
            "ha_offset (deg)",
            "dec_offset (deg)",
            "utime",
            "isotime",
            "ground_lat (deg)",
            "ground_lng (deg)",
            "ground_alt (m)",
            "aprs_lat (deg)",
            "aprs_lng (deg)",
            "aprs_alt (m)",
            "pred_lat (deg)",
            "pred_lng (deg)",
            "pred_alt (m)",
            "command",
            "source"
        ])

        while lite.live:
            loops.every_10_else()
            # Send new log[] data to .csv
            data = []
            log_data = [
                "pos",
                "azel",
                "hadec",
                "hadec_offset",
                "utime",
                "isotime",
                "ground_pos",
                "aprs_pos",
                "pred_pos",
                "command",
                "source"
            ]
            for datum in log_data:
                # Ensure string values are not extended as char arrays
                if datum == "command" or datum == "source":
                    data.append(lite.log[lite.n][datum])
                # Ensure arrays of values are stored as multiple values
                else:
                    try:
                        data.extend(lite.log[lite.n][datum])
                    except TypeError:
                        data.append(lite.log[lite.n][datum])
            writer.writerow(data)
            # Flush buffer, force write to .csv
            file.flush()
            lite.n += 1
            lite.printed = True
            time.sleep(10)
        file.close()

def auto_thread_30_aprs():
    ''' Update Ground Station data '''
    # This is a separate thread to maintain functionality in the event of errors
    loops.every_30_aprs()
    time.sleep(30)

def auto_thread_30_else():
    ''' Thread executes every 30 seconds '''
    loops.every_30_else()
    # Flush buffer, force write to output file
    lite.output_file.flush()
    # 1 second buffer after sending each commands to the telescope
    # 2 total, 1 for setting (HA, DEC) and 1 for "Go" command
    time.sleep(28)

def user_thread():
    ''' Handles mid-flight user commands '''
    # Enumerate user commands
    options = {
        "h": cmd.list_commands, "help": cmd.list_commands,
        "s": cmd.status, "status": cmd.status,
        "d": cmd.data, "data": cmd.data,
        "o": cmd.offset, "offset": cmd.offset,
        "p": cmd.pause, "pause": cmd.pause,
        "q": cmd.shutdown, "quit": cmd.shutdown,
        "r": cmd.reset, "reset": cmd.reset,
    }
    while lite.live:
        command = fcn.input_out("Type 'h' or 'help' to list commands\n")
        try:
            options[command]()
        except KeyError:
            print(fcn.print_out("Invalid command\n"))
