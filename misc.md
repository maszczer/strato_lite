# Files #
This program is comprised of several files

### main.py ###
This script will run the tracking / prediction program.

### config.py ###
Stores global variables for use by other scripts throughout the life of this program.

### threads.py ###
Three functions are called in main(), and will run simultaneously.

1. autoThread():
Runs the primary loop of the function using repeat().
This collects data from available sources,
predicts the balloon's next position,
and sends commands to orient the telescope accordingly.
Data is then output to a *.csv* file.

2. userThread():
Handles user commands that are input during runtime.

3. grndThread():
Listens on port 6001 for TCP packets from the Ground Station.

### commands.py ###
All commands called from userThread() reference functions from this file.

### functions.py ###
Contains various functions used throughout the life of this program.
Notable functions include:

- *setMode()*:
Determines if the program runs as *Test* or *Actual*.
Commands for the telescope are sent as TCP packets *only* if running as *Actual*

- *repeat()*:
This collects data from available sources,
predicts the balloon's next position,
and sends commands to orient the telescope accordingly.

### predict.py ###
Takes in *[latitude, longitude, altitude]* and returns a predicted *[latitude, longitude, altitude]*.

Credit to A. Huffman and B. Rosenbaum for the updated version.
