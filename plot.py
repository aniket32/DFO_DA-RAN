import matplotlib.pyplot as plt
import numpy as np

# Initialising random points for the users
x = np.arange(0,5)
y = np.random.randint(0,15, size=5)


ax = plt.subplot()
# Plot labels and plot type
# plt.scatter(x, y, color='b', marker='^')
ax.scatter(x, y, color='b')
# plt.xlabel("x")
# plt.ylabel("y")

# User Coordinates
coordinates = []
for i, j in zip(x, y):
    coordinates.append((i,j))

file = open('coordinates.txt', 'w')
for items in coordinates:
    line = ' '.join(str(x) for x in items)
    file.write(line + '\n')

file.close()

# Circumference Test
for a, b in coordinates:
    cir = plt.Circle((a,b), 1.5, color='r', fill=False)
    ax.set_aspect('equal', adjustable='datalim')
    ax.add_patch(cir)


# Show Plot
# plt.grid(True)
fig1 = plt.gcf()
plt.savefig('Users.png')
plt.show()
# plt.draw()
# Saving the plot

