import config as lite
import functions as fcn
import time

def list_commands():
    ''' List available user commands '''
    fcn.print_out("-- HELP --\n"
          "'d' or 'data' display most recent data\n"
          "'p' or 'pause' pause telescope movement (toggles on/off)\n"
          "'o' or 'offset' change offset to HA, DEC\n"
          "'r' or 'reset' orient telescope to default position\n"
          "'s' or 'status' display flight setup info\n"
          "'q' or 'quit' quit program\n")

def status():
    ''' Print flight setup info '''
    fcn.print_out("-- STATUS --\n"
          "APRS key: " + lite.aprs_key + "\n" +
          "Telescope coordinates : [" + str(lite.ref_pos[0]) + ", " +
          str(lite.ref_pos[1]) + ", " + str(lite.ref_pos[2]) + "]\n" +
          "TCP_IP: " + lite.TCP_IP + "\n" +
          "TCP_PORT: " + str(lite.TCP_PORT) + "\n" +
          "Program has been running for " +
          str(round(lite.n * 10 / 60, 4)) + " min")  # buggy

def print_pos(pos):
    ''' Returns string for printing latitude, longitude, altitude '''
    data = "  LAT: " + str(pos[0]) + " deg\n" + \
           "  LNG: " + str(pos[1]) + " deg\n" + \
           "  ALT: " + str(pos[2]) + " m\n"
    return data

def data():
    ''' Print most recent data, more detailed than standard output '''
    if lite.printed and lite.n > 0:
        i = lite.n - 1
        fcn.print_out("-- DATA --\n"
              "Using " + lite.log[i]['source'] + " data:\n" +
              "Sent:\n" + print_pos(lite.log[i]['pos']) +
              " TIME: " + str(lite.log[i]['utime']) + "\n" +
              "   AZ: " + str(lite.log[i]['azel'][0]) + " deg\n" + \
              "   EL: " + str(lite.log[i]['azel'][1]) + " deg\n" + \
              "RANGE: " + str(lite.log[i]['azel'][2]) + " m\n" +
              "   HA: " + str(lite.log[i]['hadec'][0]) + " deg" +
              " w/ offset " + str(lite.log[i]['hadec_offset'][0]) + "\n"
              "  DEC: " + str(lite.log[i]['hadec'][1]) + " deg" +
              " w/ offset " + str(lite.log[i]['hadec_offset'][1]) + "\n" +
              "Predicted:\n" + print_pos(lite.log[i]['pred_pos']) +
              "APRS.fi:\n" + print_pos(lite.log[i]['aprs_pos']) +
              "Ground Station:\n" + print_pos(lite.log[i]['ground_pos']) +
              ">> " + lite.log[i]['command'])
        if lite.last_ground_update == 0:
            fcn.print_out("Ground Station data is up to date")
        else:
            fcn.print_out("Calls since last Ground Station update: " + str(lite.last_ground_update))

        if lite.last_aprs_udate == 0:
            fcn.print_out("APRS data is up to date")
        else:
            fcn.print_out("Calls since last APRS update: " + str(lite.last_aprs_udate))
        fcn.print_out(str(lite.log[i]['isotime']))
        if lite.pause:
            fcn.print_out("Telescope movement is paused\n")
        else:
            fcn.print_out("Telescope movement is active\n")
    else:
        fcn.print_out("Loading data, please wait and try again\n")

def offset():
    ''' Change offset for HA, DEC '''
    fcn.print_out("-- OFFSET --\n"
          " HA offset = " + str(lite.offset_ha) +
          "DEC offset = " + str(lite.offset_dec))
    ha = lite.try_float(lite.offset_ha, "HA", "Enter new HA offset\n")
    dec = lite.try_float(lite.offset_dec, "DEC", "Enter new DEC offset\n")
    if ha == lite.offset_ha and dec == lite.offset_dec:
        fcn.print_out("(HA, DEC) offset unchanged\n")
    else:
        confirm = fcn.input_out("(HA, DEC) offset will change to (" + ha + ", " + dec + ")\n"
                            "Are you sure? Typ e'yes' to change, anything else to cancel\n")
        str_output = ""
        if confirm.lower().strip() == "yes":
            lite.offset_ha = ha
            lite.offset_dec = dec
            str_output += "Offset changed to("
        else:
            str_output += "Offset unchanged, still("
        str_output += str(lite.offset_ha) + ", " + str(lite.offset_dec) + ")\n"
        fcn.print_out(str_output)

def pause():
    ''' Pause/resume telescope movement '''
    fcn.print_out("-- PAUSE --\n")
    if not lite.pause:
        lite.pause = True
        fcn.print_out("Telescope movement is paused\n")
    else:
        lite.pause = False
        fcn.print_out("Resuming telescope movement ....\n")

def shutdown():
    ''' End program '''
    confirm = fcn.input_out("-- QUIT --\n"
                    "Are you sure you want to quit?\n"
                    "Type 'yes' to quit, anything else to cancel\n")
    if confirm.lower() == "yes":
        fcn.print_out("Quitting ....")
        if lite.is_tcp_set(lite.TCP_IP, lite.TCP_PORT):
            lite.sock.close()
        lite.output_file.close()
        lite.live = False
    else:
        fcn.print_out("Resuming tracking ....\n")

def reset():
    ''' Send telescope to HA 3.66 and DEC -6.8 '''
    confirm = fcn.input_out("-- RESET --\n"
                    "Are you sure you want to reset orientation to the default position?\n"
                    "Type 'yes' to move, anything else to cancel\n")
    if confirm.lower() == "yes":
        # '#33,HA,DEC;' Provides values for HA, DEC to telescope
        # This should be the default position for the telescoep
        command = "#33,3.66,-6.8;"
        fcn.print_out(">> " + command)
        if lite.is_tcp_set(lite.TCP_IP, lite.TCP_PORT) and not lite.pause:
            lite.sock.send(bytes(command, 'utf-8'))
            time.sleep(1)
            # '#12;' Commands telescope to point towards current HA, DEC
            command = "12;"
            lite.sock.send(bytes(command, 'utf-8'))
            time.sleep(1)
    else:
        fcn.print_out("Resuming tracking ....\n")