import time

# Simulate .log file by outputting values every 10 seconds
filename_out = "testing_log_generator_from_existing.log"
# Pulls data from existing flight data
filename_in = input("Enter existing .log filename\n")
file_in = open(filename_in, 'r')
i = 0
data = ""
while True:
    file_out = open(filename_out, 'w')
    print(str(i) + "...")
    row = file_in.readline()
    data += row
    file_out.write(data)
    file_out.flush()
    file_out.close()
    time.sleep(10)