import matplotlib.pyplot as plt
import numpy as np

# Extra parameters
# plt.rcParams["figure.figsize"] = [7, 7]
# plt.rcParams["figure.autolayout"] = True

# Initialising random points for the users
x = np.arange(50)
y = np.random.randint(20, size=50)

# Plot labels and plot type
plt.scatter(x, y, color='b', marker='^')
plt.xlabel("x")
plt.ylabel("y")

# User Coordinates
coordinates = []
for i, j in zip(x, y):
    coordinates.append([i, j])

# Show Plot
plt.grid(True)
plt.show()
# Saving the plot
# plt.savefig("Users.png")
