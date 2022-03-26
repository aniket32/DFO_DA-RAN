import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.art3d as art3d

# Initialising random points for the users
x = np.random.randint(0, 40, size=10)
y = np.random.randint(0, 40, size=10)
z = np.random.randint(0, 40, size=10)

ax = plt.subplot(projection='3d')
# Plot labels and plot type
# plt.scatter(x, y, color='b', marker='^')
ax.scatter(x, y, z, color='b')
# plt.xlabel("x")
# plt.ylabel("y")

# User Coordinates
coordinates = []
for i, j, k in zip(x, y, z):
    coordinates.append((i, j, k))
print(coordinates)

# with open("coordinates.csv", "w", newline=' ') as f:
#     wr = csv.writer(f, delimiter = ",")
#     wr.writerows(coordinates)

# file = open('coordinates.txt', 'w')
# for items in coordinates:
#     line = ' '.join(str(x) for x in items)
#     file.write(line + '\n')
# file.close()

# Circumference Test
for a, b, c in coordinates:
    cir = plt.Circle((a, b), 1.5, color='r', fill=False)
    # ax.set_aspect('equal', adjustable='datalim')
    ax.add_patch(cir)
    art3d.pathpatch_2d_to_3d(cir, z = c, zdir="z")

# Show Plot
# plt.grid(True)
fig1 = plt.gcf()
plt.show()
# plt.draw()
# Saving the plot
