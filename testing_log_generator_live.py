import time

# Simulate .log file by outputting values every 10 seconds
filename = "testing_log_generator_live.log"
i = 0
data = ""
while True:
    file = open(filename, 'w')
    print(str(i) + " ...")
    # Set variables
    latitude = str(i + 100)
    longitude = str(i + 200)
    altitude = str(i ** 2)
    utime = str(i)
    # Callsign to track
    source = "T35T1N6"
    # Dummy callsign to cause no update
    if i % 5 == 0:
        source = "F4K"
    # chan,utime,isotime,source,heard,level,error,dti,name,symbol,latitude,longitude,speed,course,altitude,frequency,offset,tone,system,status,comment
    data += ',' + utime + ',,' + source + ',,,,,,,' + latitude + ',' + longitude + ',,,' + altitude + '\n'
    i += 1
    file.write(data)
    file.flush()
    file.close()
    time.sleep(10)
