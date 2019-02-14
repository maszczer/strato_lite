# Getting Started #
This program tracks an APRS callsign and calculates its next predicted position.
It then sends commands to orient a telescope towards this position over TCP/IP on socket.
Data is also saved throughout the duration of the flight, and is output to a *.csv* file.

Run this with
```
python3 main.py
```

For making a prediction, data will be retrieved from one of the following methods:

- Ground Station, which transmits data to port 6001 on your localhost
- APRS, which updates approximately every 30 sec
- Previous predicted values

The source used for a prediction will depend on what *new* data is available,
and will be chosen from those listed with respective decreasing priority.



# Required Modules #

- *csv*
- *datetime*
- *math*
- *numpy*
- *pymap3d*
- *queue*
- *socket*
- *time*
- *urllib*
- *threading*

NOTE: All these packages are available in PyCharm

# Other Requirements #
- A registered key is required for use with *APRS.fi* for callsign tracking
- *predict.py* which takes in *[latitude, longitude, altitude]*
and returns a predicted *[latitude, longitude, altitude]*

# Required Inputs #
At runtime, the following will be required to begin tracking / prediction:

- APRS key
- Geodetic coordinates of the telescope (latitude, longitude, altitude)
- APRS callsign to track
- Mode, which can be run as *test* or *actual*
     - *Test*: track an APRS callsign and output data to the terminal and a *.csv* file
     - *Actual*: perform the same functions as *Test* mode, but also output telescope-commands to a specified IP address & port number
- IP address & port number for the computer connected to the telescope  (*Actual* mode only)

# In-flight Commands #
While this program is running, the following commands can be used:

- *'d'* or *'data'*: displays the most recently calculated data
- *'p'* or *'pause'*: pauses telescope movement (toggles on / off)
- *'o'* or *'offset'*: change an applied offset to the predicted Hour Angle & Declination
- *'r'* or *'reset'*: orient telescope to its default position (3.66, -6.8)
- *'s'* or *'status'*: Display flight setup info
- *'q'* or *'quit'*: exits the program

For further reading on how this program is structured, see *program_structure.md*
