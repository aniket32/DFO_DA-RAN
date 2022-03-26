# IMPORTING THE MODULES
import math
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d

# RANDOM INITIALIZATIONS OF THE USER COORDINATES
x_coor = np.random.randint(0, 3000, size=20)
y_coor = np.random.randint(0, 3000, size=20)

coordinates = []  # ARRAY TO STORE THE USER COORDINATES
for i, j in zip(x_coor, y_coor):
    coordinates.append((i, j))

file = open('coordinates.txt', 'w')
for items in coordinates:
    line = ' '.join(str(x) for x in items)
    file.write(line + '\n')
file.close()

# EXPERIMENTAL PARAMETERS BASED ON THE SUB-URBAN ENVIRONMENT
thita_opt = 0.35499997  # OPTIMAL ELEVATION ANGLE
a = 4.88  # CONSTANT VALUE
b = 0.43  # CONSTANT VALUE
A = -23.39  # CONSTANT VALUE
B = 4.14  # CONSTANT VALUE
P_LoS = 0.0001  # PROBABILITY OF LINE OF SIGHT
P_NLoS = 21  # PROBABILITY OF NON LINE OF SIGHT
f_c = 2.4  # CARRIER FREQUENCY
c = 3000  # SPEED OF LIGHT
A_1 = P_LoS - P_NLoS
B_1 = 20 * math.log10((4 * math.pi * f_c) / c) + P_LoS


# R = 395  # COVERAGE RADIUS

# FITNESS FUNCTION
def f(x):  # x IS THE COORDINATED OF ONE FLY
    yes = 0
    for items in coordinates:
        # USER COORDINATE
        x_i = items[0]
        y_i = items[1]
        for i in range(N):
            x_d = x[1]  # FLY/DRONE X COORDINATE
            y_d = x[0]  # FLY/DRONE Y COORDINATE
            R = radius[i]  # FLY/DRONE COVERAGE RADIUS
            # CHECKING IF THE USER IS WITHIN THE COVERAGE RADIUS OF THE DRONE/FLY
            coverage = ((x_i - y_d) ** 2 + (y_i - x_d) ** 2)
            # IF USER USER WITHIN THE COVERAGE RADIUS COUNTER INCREMENT BY 1
            if coverage <= R * R:
                yes += 1
    return yes


# COVERAGE RADIUS FUNCTION
def rad(x):  # X IS THE PATHLOSS OF ONE FLY
    r = 0.0
    for i in range(len(x)):
        # FINDING THE COVERAGE RADIUS OF EACH DONE IN ACCORDANCE WITH THE PATHLOSS VALUE
        r = (-(20 * A_1) / (1 + a * math.exp(-b * (((180 / math.pi) * thita_opt) - a))) - (B_1 / 20) + (
                x[2] / 20)) * math.cos(thita_opt)
    return r


N = 10  # POPULATION SIZE
D = 3  # DIMENSIONALITY
delta = 0.01  # DISTURBANCE THRESHOLD
maxIterations = 1200  # ITERATIONS ALLOWED
lowerB = [0, 0, 0]  # LOWER BOUND (IN ALL DIMENSIONS)
upperB = [3000, 3000, 89]  # UPPER BOUND (IN ALL DIMENSIONS)

# INITIALISATION PHASE
X = np.empty([N, D])  # EMPTY FLIES ARRAY OF SIZE: (N,D)
fitness = [None] * N  # EMPTY FITNESS ARRAY OF SIZE N
radius = [None] * N  # EMPTY COVERAGE RADIUS ARRAY OF SIZE N
height = []  # EMPTY HEIGHT ARRAY

# INITIALISE FLIES WITHIN BOUNDS
for i in range(N):
    for d in range(D):
        X[i, d] = np.random.uniform(lowerB[d], upperB[d])

# FINDING THE COVERAGE RADIUS OF FLY/DRONE
for i in range(N):
    radius[i] = rad(X[i,])

# HEIGHT OF EACH FLY/DRONE IN ACCORDANCE WITH CIVERAGE RADIUS
for y in radius:
    h = y * math.tan(thita_opt)
    height.append(h)
print(height, "height")

# MAIN DFO LOOP
for itr in range(maxIterations):
    ax = plt.subplot()
    ax.scatter(x_coor, y_coor, color='b', marker='^')
    plt.draw()
    plt.show(block=False)

    for i in range(N):  # EVALUATION
        fitness[i] = f(X[i,])
    s = np.argmax(fitness)  # FIND BEST FLY

    if itr % 300 == 0:  # PRINT BEST FLY EVERY 300 ITERATIONS
        print("Iteration:", itr, "\tBest fly index:", s,
              "\tFitness value:", fitness[s])

    # TAKE EACH FLY INDIVIDUALLY
    for i in range(N):
        if i == s: continue  # ELITIST STRATEGY

        # FIND BEST NEIGHBOUR
        left = (i - 1) % N
        right = (i + 1) % N
        bNeighbour = right if fitness[right] < fitness[left] else left

        for d in range(D):  # UPDATE EACH DIMENSION SEPARATELY
            if np.random.rand() < delta:
                X[i, d] = np.random.uniform(lowerB[d], upperB[d])
                continue;

            u = np.random.rand()
            X[i, d] = X[bNeighbour, d] + u * (X[bNeighbour, d] - X[i, d])

            # OUT OF BOUND CONTROL
            if X[i, d] < lowerB[d] or X[i, d] > upperB[d]:
                X[i, d] = np.random.uniform(lowerB[d], upperB[d])

    # PLOTTING THE BEST FLY
    rowNo = X[s, 0]  # BEST FLY X COORDINATE
    colNo = X[s, 1]  # BEST FLY Y COORDINATE
    swarmBestCircle = plt.Circle((rowNo, colNo), 10, color='r')
    # COVERAGE RADIUS FOR THE BEST DRONES IN THE PLOT
    cir = plt.Circle((rowNo, colNo), radius[s], color='y', fill=False)
    ax.set_aspect('equal', adjustable='datalim')
    ax.add_patch(cir)

    # for a, b in zip(rowNo,colNo):
    #     print(a,b)

    # PLOTTING ALL THE FLY
    circle = []
    for i in range(N):
        circle.append(plt.Circle((X[i, 0], X[i, 1]), 10, color='g'))
        plt.gca().add_patch(circle[i])
        # COVERAGE RADIUS FOR ALL THE DRONES IN THE PLOT
        cir = plt.Circle((X[i, 0], X[i, 1]), radius[i], color='y', fill=False)
        ax.set_aspect('equal', adjustable='datalim')
        ax.add_patch(cir)

    plt.gca().add_patch(swarmBestCircle)  # ADD THE CIRCLE
    plt.draw()  # DRAW THE IMAGE AND THE CIRCLE
    plt.xlim([0, 3000])  # LIMITING THE PLOT FROM 0 TO 3000 IN X ASIS
    plt.ylim([0, 3000])  # LIMITING THE PLOT FROM 0 TO 3000 IN Y ASIS
    plt.show(block=False)
    plt.pause(0.01)
    plt.clf()  # CLEARING THE CANVAS

    # drone_coor = []
    # new_coor = []
    # if itr == 300:
    #     for i in range(N):
    #         fitness[i] = f(X[i,])  # EVALUATION
    #         s = np.argmax(fitness)
    #         x_d = X[s, 0]
    #         y_d = X[s, 1]
    #         for items in coordinates:
    #             x_i = items[0]
    #             y_i = items[1]
    #             coverage = ((x_i - y_d) ** 2 + (y_i - x_d) ** 2)
    #             if coverage <= R * R:
    #                 drone_coor.append((x_d, y_d))
    #                 new_coor.append((x_i, y_i))
    #
    #     print(drone_coor, "drone")
    #     print(new_coor, "users")

for i in range(N): fitness[i] = f(X[i,])  # EVALUATION
s = np.argmax(fitness)  # FIND BEST FLY

print("\nFinal best fitness:\t", fitness[s])
print("\nBest fly position:\n", X[s,])
