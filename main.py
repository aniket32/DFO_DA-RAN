import math
import numpy as np
import matplotlib.pyplot as plt

# RANDOMIZING X AND Y COORDINATES
x_coor = np.random.randint(0, 2000, size=10)
y_coor = np.random.randint(0, 2000, size=10)

# PLOT LABELS
plt.xlabel("x")
plt.ylabel("y")

# USER COORDINATES
coordinates = []
for i, j in zip(x_coor, y_coor):
    coordinates.append((i, j))

# SAVING THE USER COORDINATES IN A TEST FILE
file = open('coordinates.txt', 'w')
for items in coordinates:
    line = ' '.join(str(x) for x in items)
    file.write(line + '\n')
file.close()

# PARAMETERS
thita_opt = 0.35499997
a = 4.88
b = 0.43
A = -23.39
B = 4.14
P_LoS = 0.1
P_NLoS = 21
f_c = 2.4
c = 3000
A_1 = P_LoS - P_NLoS
B_1 = 20 * math.log10((4 * math.pi * f_c) / c) + P_LoS


def remover(lst):
    return list(set([i for i in lst]))


# FITNESS FUNCTION
# PATHLOSS THRESHOLD IS X
def f(x):  # x IS A VECTOR REPRESENTING ONE FLY
    best = []
    yes = 0
    no = 0
    # R = 0.0
    # for i in range(len(x)):
    #     R = (-(20 * A_1) / (1 + a * math.exp(-b * (((180 / math.pi) * thita_opt) - a))) - (B_1 / 20) + (
    #             x[0] / 20)) * math.cos(thita_opt)

    for items in coordinates:
        x_i = items[0]
        y_i = items[1]
        for i in range(N):
            x_d = X[i, 1]
            y_d = X[i, 0]
            coverage = ((x_i - x_d) ** 2 + (y_i - y_d) ** 2)
            if coverage <= 395 ** 2:
                yes += 1

    #             drone_coor.append(((x_d, y_d),(x_i, y_i)))
    #
    # print(drone_coor, "drone-user")

    # print(drone_coor,"drone", user_coor, "user")
    return yes


N = 1  # POPULATION SIZE
D = 2  # DIMENSIONALITY
delta = 0.0001  # DISTURBANCE THRESHOLD
maxIterations = 700  # ITERATIONS ALLOWED

# DC PATHLOSS CONSTRAINTS
lowerB = [0, 0]  # LOWER BOUND (IN ALL DIMENSIONS)
upperB = [2000, 2000]  # UPPER BOUND (IN ALL DIMENSIONS)

# DRONE COORDINATES
# coorU = [0, 0]
# coorL = [2000, 2000]

# INITIALISATION PHASE
X = np.empty([N, D])  # EMPTY FLIES ARRAY OF SIZE: (N,D)
fitness = [None] * N  # EMPTY FITNESS ARRAY OF SIZE N

# ARRAY FOR THE DRONES COORDINATES
# Y = np.empty([N, 2])

# INITIALISE FLIES WITHIN BOUNDS
for i in range(N):
    for d in range(D):
        X[i, d] = np.random.randint(lowerB[d], upperB[d])
        # print(X[i,d],"Xid")

# for j in range(N):
#     Y[j] = np.random.uniform(coorU, coorL)
# print(Y[j], "Yj")

# ax.scatter(x_coor, y_coor, color='b', marker='^')
# plt.draw()
# plt.show(block=False)
# MAIN DFO LOOP
for itr in range(maxIterations):
    ax = plt.subplot()
    ax.scatter(x_coor, y_coor, color='b', marker='^')
    plt.draw()
    plt.show(block=False)

    for i in range(N):  # EVALUATION
        fitness[i] = f(X[i])
        print(fitness,"fit")
    s = np.argmax(fitness)  # FIND BEST FLY

    if itr % 100 == 0:  # PRINT BEST FLY EVERY 100 ITERATIONS
        print("Iteration:", itr, "\tBest fly index:", s,
              "\tFitness value:", fitness[s])

    # TAKE EACH FLY INDIVIDUALLY
    for i in range(N):
        if i == s: continue  # ELITIST STRATEGY

        # FIND BEST NEIGHBOUR
        left = (i - 1) % N
        right = (i + 1) % N
        bNeighbour = right if fitness[right] > fitness[left] else left

        for d in range(D):  # UPDATE EACH DIMENSION SEPARATELY
            if np.random.rand() < delta:
                X[i, d] = np.random.randint(lowerB[d], upperB[d])
                continue;

            u = np.random.rand()
            X[i, d] = X[bNeighbour, d] + u * (X[bNeighbour, d] - X[i, d])

            # OUT OF BOUND CONTROL
            if X[i, d] < lowerB[d] or X[i, d] > upperB[d]:
                X[i, d] = np.random.randint(lowerB[d], upperB[d])

    rowNo = X[s, 0]
    colNo = X[s, 1]
    swarmBestCircle = plt.Circle((rowNo, colNo), 10, color='r')
    # COVERAGE RADIUS FOR THE DRONES IN THE PLOT
    cir = plt.Circle((rowNo, colNo), 395, color='y', fill=False)
    ax.set_aspect('equal', adjustable='datalim')
    ax.add_patch(cir)

    # for a, b in zip(rowNo,colNo):
    #     print(a,b)

    # THIS SECTION IS OPTIONAL TO SHOW ALL FLIES
    circle = []
    for i in range(N):
        circle.append(plt.Circle((X[i, 0], X[i, 1]), 10, color='g'))
        plt.gca().add_patch(circle[i])
        # COVERAGE RADIUS FOR THE DRONES IN THE PLOT
        cir = plt.Circle((X[i, 0], X[i, 1]), 395, color='y', fill=False)
        ax.set_aspect('equal', adjustable='datalim')
        ax.add_patch(cir)

    plt.gca().add_patch(swarmBestCircle)  # ADD THE CIRCLE
    plt.draw()  # DRAW THE IMAGE AND THE CIRCLE
    plt.show(block=False)
    plt.pause(0.01)  # PAUSE BEFORE THE NEXT ITERATION IN BETWEEN
    plt.clf()  # CLEAR THE CANVAS
    # ax.grid(True)

    # for a in range(maxIterations):
    #     ax.scatter(x_coor, y_coor, color='b', marker='^')
    #     plt.draw()
    #     plt.show(block=False)

for i in range(N):
    fitness[i] = f(X[i,])  # EVALUATION
s = np.argmax(fitness)

# FIND BEST FLY
print("\nFinal best fitness:\t", fitness[s])
print("\nBest fly position:\n", X[s,])

# FIND THE TOTAL CIRCUMFERENCE
print("\nTotal circumference:\n", 2 * math.pi * fitness[s])

# FIND THE OPTIMAL HEIGHT OF THE BEST DRONE
print("\nHeight:\n", fitness[s] * math.tan(thita_opt))
