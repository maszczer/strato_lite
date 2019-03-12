# Files #
This program is comprised of several files

### main.py ###
Runs the program using a series of threads.
- Thread-1 `auto_thread_30_aprs`: Updates data from APRS.fi every 30 seconds
- Thread-2 `auto_thread_10_ground`: Updates data from Ground Station `.log` file every 10 seconds
- Thread-3 `auto_thread_10_else`: Updates predicted position, writes data to `lite.log`
- Thread-4 `auto_thread_30_else`: Sends command to telescope
- Main Thread `user_thread`: Handles real-time user commands

### config.py ###
Stores global variables for use by other scripts throughout the life of this program.

NOTE: Predicted positions are made 30 seconds ahead of time, thus a queue is used for storing these values.

### threads.py ###
Functions which run within each of the threads in `main.py`.

### loops.py ###
Functions which are repeatedly called within each of the `while` loops in `threads.py`. These do differ from the functions in `threads.py`, as they *only* contain actions which will occur repeatedly.

### functions.py ###
Various helper functions used throughout the life of this program. These are used for tasks such as unit conversions, printing to both the terminal and output files, and data retrieval and updates.

### commands.py ###
The various user commands which can be used at runtime.

### predict.py ###
Takes in `[latitude, longitude, altitude]` and returns a predicted `[latitude, longitude, altitude]`. If a predicted position is invalid, it will be set to `[-404, -404, -404]`.

Credit to A. Huffman and B. Rosenbaum for the updated version of `predict.py`.
