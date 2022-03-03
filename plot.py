import matplotlib.pyplot as plt
import numpy as np

# Extra parameters
# plt.rcParams["figure.figsize"] = [7, 7]
# plt.rcParams["figure.autolayout"] = True

# Initialising random points for the users
x = np.arange(40)
y = np.random.randint(20, size=40)

# Plot labels and plot type
plt.scatter(x, y, color='b', marker='^')
plt.xlabel("x")
plt.ylabel("y")

# User Coordinates
coordinates = []
for i, j in zip(x, y):
    coordinates.append((i,j))

file = open('coordinates.txt', 'w')
for items in coordinates:
    line = ' '.join(str(x) for x in items)
    file.write(line + '\n')

# for items in coordinates:
#     print(items)

# Show Plot
# plt.grid(True)
fig1 = plt.gcf()
plt.savefig('Users.png')
plt.show()
plt.draw()
# Saving the plot

