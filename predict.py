import functions as fcn
import config as lite
from astropy import units as u
from astropy.coordinates import EarthLocation
import numpy as np

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
## return pos for first 30 sec
# An algorithm for predicting the balloon's next location
def predict(pos):
    # Start prediction after 30 seconds have elapsed
    if lite.n < 3\
            or not np.array_equal(lite.log[-1]['pos'][0:3], lite.null_pos[0:3])\
            or not np.array_equal(lite.log[-2]['pos'][0:3], lite.null_pos[0:3])\
            or not np.array_equal(lite.log[-3]['pos'][0:3], lite.null_pos[0:3]):
        return pos
    n = lite.n
    try:
        ## MAKE ALL CHANGES BELOW ##
        ############################
        if (n > 0):
            dt = 10
            dtpred = 30
            u_0lla = lite.log[-1]["pos"][0:3]
            u_0xyz = EarthLocation(lat=u_0lla[0], lon=u_0lla[1], height=u_0lla[2]*u.m)
            u_0xyz = [u_0xyz.x.value,u_0xyz.y.value,u_0xyz.z.value]

            u_1lla = lite.log[-2]["pos"][0:3]
            u_1xyz = EarthLocation(lat=u_1lla[0], lon=u_1lla[1], height=u_1lla[2]*u.m)
            u_1xyz = [u_1xyz.x.value,u_1xyz.y.value,u_1xyz.z.value]

            u_2lla = lite.log[-3]["pos"][0:3]
            u_2xyz = EarthLocation(lat=u_2lla[0], lon=u_2lla[1], height=u_2lla[2]*u.m)
            u_2xyz = [u_2xyz.x.value,u_2xyz.y.value,u_2xyz.z.value]

            d_0 = 3.0/(2.0*dt)
            d_1 = -2.0/dt
            d_2 = 1.0/(2.0*dt)

            dUdt_x = d_0*u_0xyz[0]+d_1*u_1xyz[0]+d_2*u_2xyz[0]
            dUdt_y = d_0*u_0xyz[1]+d_1*u_1xyz[1]+d_2*u_2xyz[1]
            dUdt_z = d_0*u_0xyz[2]+d_1*u_1xyz[2]+d_2*u_2xyz[2]

            xPred = u_0xyz[0]+dtpred*dUdt_x
            yPred = u_0xyz[1]+dtpred*dUdt_y
            zPred = u_0xyz[2]+dtpred*dUdt_z

            uPredxyz = EarthLocation(x=u_1lla[0]*u.m, y=u_1lla[1]*u.m, z=u_1lla[2]*u.m)
            uPredlla = uPredxyz.to_geodetic('WGS84')
            predLat = uPredlla.lat.value
            predLng = uPredlla.lon.value
            predAlt = uPredlla.height.value

        ############################
        ## MAKE ALL CHANGES ABOVE ##
    except IndexError:
        pass
    return [(predLat), (predLng), (predAlt)]
