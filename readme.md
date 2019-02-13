# Getting Started #
This program tracks an APRS callsign and calculates its next predicted position.
It then sends commands to orient a telescope towards this position over TCP/IP on socket.
Data is also saved throughout the duration of the flight, and is output to a *.csv* file.

Run this with
```
python3 main.py
```

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

# Inputs #
...
