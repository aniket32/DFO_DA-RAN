# IMPORTING THE LIBRARIES
import csv
import numpy as np
import matplotlib.pyplot as plt

# PLOTTING THE GRAPH IN 2D
ax = plt.subplot()

# READING FROM CSV TO AN ARRAY
coordinates = np.genfromtxt('coordinates.csv', delimiter=',')
f = open('coordinates.csv')
reader = csv.reader(f)
lines = len(list(reader))
for i, j in coordinates:
    x_coor = i # USER X COORDINATE
    y_coor = j # USER Y COORDINATE
    ax.scatter(x_coor, y_coor, color='b', marker='^')

# READING FROM CSV TO AN ARRAY
best_drone = np.genfromtxt('best_drones.csv', delimiter=',')
for i,j,k,l in best_drone:
    x_d = i # DRONE X COORDINATE
    y_d = j # DRONE Y COORDINATE
    R = l   # DRONE COVERAGE RADIUS
    ax.scatter(x_d, y_d, color='r')
    # COVERAGE RADIUS OF THE DRONES/FLY
    cir = plt.Circle((x_d, y_d), R, color='y', fill=False)
    ax.set_aspect('equal', adjustable='datalim')
    ax.add_patch(cir)


# SHOW PLOT
plt.xlim([0, 3000])  # LIMITING THE PLOT FROM 0 TO 3000 IN X ASIS
plt.ylim([0, 3000])  # LIMITING THE PLOT FROM 0 TO 3000 IN Y AXIS
plt.show()
plt.draw()