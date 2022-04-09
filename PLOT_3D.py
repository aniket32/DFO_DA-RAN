# IMPORTING THE LIBRARIES
import os
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d

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

bs_xcoor = x_limit / 2
bs_ycoor = y_limit / 2


# PLOTTING THE GRAPH IN 3D
ax = plt.subplot(projection='3d')

# PLOTTING THE BASE STATION
ax.scatter(bs_xcoor, bs_ycoor, 200, color='r', marker='^')
# PLOTTING THE BASE STATION COVERAGE RANGE
cir = plt.Circle((bs_xcoor, bs_ycoor), 2500, color='y', fill=False)
ax.add_patch(cir)
# ax.set_aspect('equal', adjustable='datalim')
# PLOTTING THE OPERATIONAL RANGE OF DRONES
c = plt.Circle((bs_xcoor, bs_ycoor), max_R_DB, color='r', fill=False)
ax.add_patch(c)
# ax.set_aspect('equal', adjustable='datalim')
art3d.pathpatch_2d_to_3d(cir, z=200, zdir="z")
art3d.pathpatch_2d_to_3d(c, z=200, zdir="z")


# READING FROM CSV TO AN ARRAY
coordinates = np.genfromtxt('cov_users.csv', delimiter=',')
f = open('coordinates.csv')
reader = csv.reader(f)
lines = len(list(reader))
# PLOTTING COVERED USERS
for i, j in coordinates:
    x_coor = i # USER X COORDINATE
    y_coor = j # USER Y COORDINATE
    for i in range(lines):
        z_coor = 0
        ax.scatter(x_coor, y_coor, z_coor, color='b', marker=',')

# PLOTTING UNCOVERED USERS
if os.stat(path).st_size ==0:
    print("All users are covered")
else:
    uncov_users = np.genfromtxt('ucov_users.csv', delimiter=',')
    for i, j in uncov_users:
        ux_coor = i  # USER X COORDINATE
        uy_coor = j  # USER Y COORDINATE
        for i in range(lines):
            uz_coor = 0
            ax.scatter(ux_coor, uy_coor,uz_coor, color='r', marker=',')

# READING FROM CSV TO AN ARRAY
best_drone = np.genfromtxt('best_drones.csv', delimiter=',')
for m,n,o in best_drone:
    x_d = m # DRONE X COORDINATE
    y_d = n # DRONE Y COORDINATE
    z_d = o # DROVE Z COORDINATE  # DRONE COVERAGE RADIUS
    ax.scatter(x_d, y_d, z_d, color='r')
    # COVERAGE RADIUS OF THE DRONES/FLY
    cir = plt.Circle((x_d, y_d), r, color='y', fill=False)
    ax.add_patch(cir)
    # PLOTTING THE COVERAGE IN ACCORDANCE WITH Z AXIS
    art3d.pathpatch_2d_to_3d(cir, z=z_d, zdir="z")

# SHOW PLOT
plt.xlim([0, 5000])  # LIMITING THE PLOT FROM 0 TO 3000 IN X ASIS
plt.ylim([0, 5000])  # LIMITING THE PLOT FROM 0 TO 3000 IN Y AXIS
plt.show()
plt.draw()

