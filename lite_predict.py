import lite_config as c
import lite_functions as fcn

# User instrucitons
'''
WHAT YOU NEED TO KNOW BEFORE
IMPLEMENTING A NEW PREDICTION ALGORITHM
---------------------------------------
You will need to reference lite_config.py for global variables
All flight data will be stored in this file

REFERENCING DATA
----------------
Data is stored in a 2D array. Access it using
    c.log[i]
where 'i' indicates data stored at the ith interval
NOTE: Indexing begins at i = 0

The balloon's starting coordinates (geodetic) is not stored globally
It is referenced by using
    pos

GEODETIC COORDINATES
-----------------------------
To use data from the ith interval, use
    c.log[i][j]
where 'j' indicates the latitude, longitude, or altitude
    latitude:  j = 0
    longitude: j = 1
    altitude:  j = 2

The balloon's starting coordinates (geodetic) can be referenced using
    pos[j]
    
Previous predicted values can also be referenced from log[]
    latitude:  j = 11
    longitude: j = 12
    altitude:  j = 13
NOTE: You can only access predicted values for previous values
Attempting to access c.log[c.n][j] for j = 11, 12, or 13 will throw an error

MOST RECENT DATA
----------------
Data from the most recent interval is stored at
    c.n
Thus, you can reference the most recent data using
    c.log[c.n]

OUTPUT
------
predict() must return a list in the following form
    [a, b, c]
Where these variables represent latitude, longitude, and altitude in degrees
    a = latitude
    b = longitude
    c = altitude

------------------------------
IMPLEMENT YOUR ALGORITHM BELOW
'''

# An algorithm for predicting the balloon's next location
def predict(pos):
    if (c.n == 0):
        return pos
        ## MAKE ALL CHANGES BELOW ##
        ############################

    else:
        predLat = (c.log[c.n][0] - c.log[c.n - 1][0]) + c.log[c.n][0]
        predLng = (c.log[c.n][1] - c.log[c.n - 1][1]) + c.log[c.n][1]
        predAlt = (c.log[c.n][2] - c.log[c.n - 1][2]) + c.log[c.n][2]

        ############################
        ## MAKE ALL CHANGES ABOVE ##
        return [(predLat), (predLng), (predAlt)]