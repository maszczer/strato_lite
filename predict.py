import functions as fcn
import setup as lite

# User instructions
'''
WHAT YOU NEED TO KNOW BEFORE
IMPLEMENTING A NEW PREDICTION ALGORITHM
---------------------------------------
You will need to reference setup.py for global variables
All flight data will be stored in this file

REFERENCING DATA
----------------
Data is stored in a dictionary. Access it using
    lite.log[i]["tag"]
where 'i' indicates data stored at the ith interval
and "tag" denotes the type of data being accessed
NOTE: Indexing begins at i = 0

The balloon's current coordinates (geodetic) is not stored globally
It is referenced by using
    pos

GEODETIC COORDINATES
-----------------------------
To use data from the ith interval, use
    lite.log[i]["pos"][j]
where 'j' indicates the latitude, longitude, or altitude
    latitude:  j = 0
    longitude: j = 1
    altitude:  j = 2

The balloon's starting coordinates (geodetic) can be referenced using
    pos[j]
    
Previous predicted values can also be referenced using
    lite.log[i]["predPos"][j]

NOTE: You can only access predicted values for previous values
Attempting to access lite.log[i]["predPos"] will throw an error
You must use a time t | (t > 0) & (t < i)

MOST RECENT DATA
----------------
Data from the most recent interval is stored at
    n
Thus, you can reference the most recent data using
    lite.log[n]

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
    if (lite.n == 0):
        return pos
    else:
        n = lite.n
        predLat = pos[0]
        predLng = pos[1]
        predAlt = pos[2]
        ## MAKE ALL CHANGES BELOW ##
        ############################
        if (n > 0):
            predLat = (2 * pos[0] - lite.log[n - 1]["pos"][0])
            predLng = (2 * pos[1] - lite.log[n - 1]["pos"][1])
            predAlt = (2 * pos[2] - lite.log[n - 1]["pos"][2])

        ############################
        ## MAKE ALL CHANGES ABOVE ##
    return [(predLat), (predLng), (predAlt)]