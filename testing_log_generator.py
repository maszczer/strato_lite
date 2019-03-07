import time

# Simulate .log file by outputting values every 10 seconds
filename = "testing_log_generator.log"
file = open(filename, 'w')
i = 0
data = ""
#while True:
while i < 100:
    print(str(i) + " ...")
    datum = [0] * 15
    if i % 5 == 0:
        datum[3] = "F4K"
    else:
        datum[3] = "T35T1N6"
    datum[10] = i
    datum[11] = i + 1
    datum[14] = i ** 2
    datum[1] = i - 1
    data += str(datum) + "\n"
    i += 1
    #time.sleep(10)
file.write(str(data))
file.close()
