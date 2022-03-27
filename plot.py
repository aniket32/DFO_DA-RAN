import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.art3d as art3d
import csv

# coordinates=[]
# for i,j,k in zip(x,y,z):
#     coordinates.append((i,j,k))
#
# Writing to a csv
# with open('.csv', 'w', newline='') as file:
#     mywriter = csv.writer(file, delimiter=',')
#     mywriter.writerows(coordinates)


# Reading from a csv to an ARRAY
file = np.genfromtxt('coordinates.csv', delimiter=',')
f = open('coordinates.csv')
reader = csv.reader(f)
lines = len(list(reader))
for i, j in file:
    x_coor = i
    y_coor = j
    for i in range(lines):
        z_coor = 0
        ax = plt.subplot(projection='3d')
        ax.scatter(x_coor, y_coor, z_coor, color='b', marker='^')

# Circumference Test
# for a, b, c in coordinates:
#     cir = plt.Circle((a, b), 1.5, color='r', fill=False)
#     # ax.set_aspect('equal', adjustable='datalim')
#     ax.add_patch(cir)
#     art3d.pathpatch_2d_to_3d(cir, z=c, zdir="z")

# Show Plot
# plt.grid(True)
# fig1 = plt.gcf()
# plt.xlim([0, 3000])  # LIMITING THE PLOT FROM 0 TO 3000 IN X ASIS
# plt.ylim([0, 3000])
# plt.show()
# plt.draw()
# Saving the plot
