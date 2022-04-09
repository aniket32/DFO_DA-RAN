# IMPORTING THE LIBRARIES
import os
import math
import numpy as np
import matplotlib.pyplot as plt

path = 'ucov_users.csv'

# VARIABLES FOR CALCULATION
a = 4.88  # CONSTANT VALUE
b = 0.43  # CONSTANT VALUE
f_c = 2400  # CARRIER FREQUENCY
c = 299792458  # SPEED OF LIGHT
nLoS = 0.1  # MEAN ADDITIONAL LOSS FOR LINE OF SIGHT
nNLoS = 21  # MEAN ADDITIONAL LOS FOR NON LINE OF SIGHT
thita_opt = 0.35499997  # OPTIMAL ELEVATION ANGLE
PL_D2U_max = 89  # UPPERBOUND FOR USER TO DRONE PATHLOSS
A_1 = nLoS - nNLoS  # PARAMETER FOR COVERAGE RADIUS
B_1 = 20 * math.log10((4 * math.pi * f_c) / c) + nLoS  # PARAMETER FOR COVERAGE RADIUS
# MAX RANGE FROM DRONE TO BASE STATION
total_r_db = 1280
max_R_DB = total_r_db + 400  # TOTAL OPERATIONAL RANGE OF DRONES
# FINDING THE MAXIMUM COVERAGE RADIUS OF DRONES WHEN THE THITA_OPT AND PATHLOSS THRESHOLD IS KNOWN
r = (-(20 * A_1) / (1 + pow(a, (-b * (((180 / math.pi) * thita_opt) - a)))) - (B_1 / 20) +
     (PL_D2U_max / 20)) * math.cos(thita_opt)
h = r * math.tan(thita_opt)  # HEIGHT OF THE DRONES


# LIMITS FOR THE PLOT
x_limit = 5000
y_limit = 5000

# BASE STATION COORDINATES TO BE IN THE CENTRE OF THE PLOT
bs_xcoor = x_limit / 2
bs_ycoor = y_limit / 2

# PLOTTING THE GRAPH IN 2D
ax = plt.subplot()


# READING FROM CSV TO AN ARRAY
coordinates = np.genfromtxt('cov_users.csv', delimiter=',')
# PLOTTING THE BASE STATION
plt.scatter(bs_xcoor, bs_ycoor, color='r', marker='^')
# PLOTTING THE BASE STATION COVERAGE RANGE
cir = plt.Circle((bs_xcoor, bs_ycoor), 2500, color='y', fill=False)
ax.set_aspect('equal', adjustable='datalim')
# PLOTTING THE OPERATIONAL RANGE OF DRONES
c = plt.Circle((bs_xcoor, bs_ycoor), max_R_DB, color='r', fill=False)
ax.set_aspect('equal', adjustable='datalim')
ax.add_patch(cir)
ax.add_patch(c)


for i, j in coordinates:
    x_coor = i  # USER X COORDINATE
    y_coor = j  # USER Y COORDINATE
    plt.scatter(x_coor, y_coor, color='b', marker=',')

# CHECKING IF ALL USERS ARE COVERED OR NOT
if os.stat(path).st_size == 0:
    print("All users are covered")
else:
    uncov_users = np.genfromtxt('ucov_users.csv', delimiter=',')
    for k, l in uncov_users:
        # PLOTTING THE UNCOVERED USERS
        plt.scatter(k, l, color='r', marker=',')


# READING FROM CSV TO AN ARRAY
best_drone = np.genfromtxt('best_drones.csv', delimiter=',')
for m, n, O in best_drone:
    x_d = m  # DRONE X COORDINATE
    y_d = n  # DRONE Y COORDINATE# DRONE COVERAGE RADIUS
    ax.scatter(x_d, y_d, color='r')
    # COVERAGE RADIUS OF THE DRONES/FLY
    cir = plt.Circle((x_d, y_d), r, color='y', fill=False)
    ax.set_aspect('equal', adjustable='datalim')
    ax.add_patch(cir)

# SHOW PLOT
plt.xlim([0, 5000])  # LIMITING THE PLOT FROM 0 TO 3000 IN X ASIS
plt.ylim([0, 5000])  # LIMITING THE PLOT FROM 0 TO 3000 IN Y AXIS
plt.grid(True)
plt.show()
plt.draw()