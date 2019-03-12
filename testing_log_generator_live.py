import time

# Simulate .log file by outputting values every 10 seconds
filename = "testing_log_generator_live.log"
i = 0
data = ""
while True:
    file = open(filename, 'w')
    print(str(i) + " ...")
#chan,utime,isotime,source,heard,level,error,dti,name,symbol,latitude,longitude,speed,course,altitude,frequency,offset,tone,system,status,comment
#    ,utime,       ,source,     ,     ,     ,        ,      ,latitude,longitude,     ,      ,altitude
#,utime,,source,,,,,,latitude,longitude,,,altitude

    latitude = str(i)
    longitude = str(i + 1)
    altitude = str(i ** 2)
    utime = str(i - 1)

    source = "T35T1N6"
    if i % 5 == 0:
        source = "F4K"

    data += ',' + utime + ',,' + source + ',,,,,,,' + latitude + ',' + longitude + ',,,' + altitude + '\n'
    i += 1
    file.write(data)
    file.flush()
    file.close()
    time.sleep(10)
