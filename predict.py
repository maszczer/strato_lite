import functions as fcn
import setup as lite

# User instructions
'''
WHAT YOU NEED TO KNOW BEFORE
IMPLEMENTING A NEW PREDICTION ALGORITHM
---------------------------------------
This function will take a [latitude, longitude, altitude] as input
and return a new predicted [latitude, longitude, altitude] as output

ACCESSING DATA
----------------
You have access to the balloon's current coordinates (geodetic)
as well as all previously recorded coordinates

To access the balloon's current position, use
    pos

Data recorded previously is stored in setup.py as an array of dictionaries
You may consider these to be global variables

To access these values, use
    lite.log[i]["pos"]
where 'i' indicates data stored at the ith interval
and "pos" denotes the type of data being accessed
NOTE: Indexing begins at i = 0

GEODETIC COORDINATES
-----------------------------
The balloon's current coordinates (geodetic) can be referenced using
    pos[j]

To use data from the ith interval, use
    lite.log[i]["pos"][j]
where 'j' indicates the latitude, longitude, or altitude
    latitude:  j = 0
    longitude: j = 1
    altitude:  j = 2

Previous predicted values can also be referenced using
    lite.log[i]["predPos"][j]

RESTRICTIONS
----------------
This function is used to predict the position at iteration n
When this function is called, lite.log[n] will not contain data

To access the balloon's current position, use
    pos

You are not allowed to use
    lite.log[n]
to access data at the current iteration

You are allowed to access data from previous iterations, using
    lite.log[t]
Where t must be an integer within the bounds of (t > 0) and (t < n)
Failure to maintain this will result in
    IndexError: list out of range

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
        try:
            ## MAKE ALL CHANGES BELOW ##
            ############################
            if (n > 0):
                predLat = (2 * pos[0] - lite.log[n - 1]["pos"][0])
                predLng = (2 * pos[1] - lite.log[n - 1]["pos"][1])
                predAlt = (2 * pos[2] - lite.log[n - 1]["pos"][2])

            ############################
            ## MAKE ALL CHANGES ABOVE ##
        except IndexError:
            pass
    return [(predLat), (predLng), (predAlt)]