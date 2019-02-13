# Files #
This program is comprised of several files

### main.py ###
This script will run the tracking / prediction program.

### config.py ###
Stores global variables for use by other scripts throughout the life of this program.

### threads.py ###
Three functions are called in main(), and will run simultaneously.

1. autoThread(): Runs the primary loop of the function using repeat().
This collects data from available sources,
predicts the balloon's next position,
and sends commands to orient the telescope accordingly.
Data is then output to a *.csv* file.

2. userThread(): Handles user commands that are input during runtime.

3. grndThread(): Listens on port 6001 for TCP packets from the Ground Station.

### commands.py ###

### functions.py ###

### predict.py ###
