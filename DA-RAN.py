import math
import numpy as np
import matplotlib.pyplot as plt

x_coor = np.random.randint(0, 2000, size=10)
y_coor = np.random.randint(0, 2000, size=10)

coordinates = []
for i, j in zip(x_coor, y_coor):
    coordinates.append((i, j))

thita_opt = 0.35499997
a = 4.88
b = 0.43
A = -23.39
B = 4.14
P_LoS = 0.0001
P_NLoS = 21
f_c = 2.4
c = 3000
A_1 = P_LoS - P_NLoS
B_1 = 20 * math.log10((4 * math.pi * f_c) / c) + P_LoS
R = 395


# FITNESS FUNCTION (SPHERE FUNCTION)
def f(x):
    yes = 0
    for items in coordinates:
        x_i = items[0]
        y_i = items[1]
        for i in range(N):
            x_d = x[1]
            y_d = x[0]
            coverage = ((x_i - x_d) ** 2 + (y_i - y_d) ** 2)
            if coverage <= R ** 2 or -(R ** 2) >= coverage:
                yes += 1

    return yes


N = 2  # POPULATION SIZE
D = 2  # DIMENSIONALITY
delta = 0.1  # DISTURBANCE THRESHOLD
maxIterations = 500  # ITERATIONS ALLOWED
lowerB = [0] * D  # LOWER BOUND (IN ALL DIMENSIONS)
upperB = [2000] * D  # UPPER BOUND (IN ALL DIMENSIONS)

# INITIALISATION PHASE
X = np.empty([N, D])  # EMPTY FLIES ARRAY OF SIZE: (N,D)
fitness = [None] * N  # EMPTY FITNESS ARRAY OF SIZE N
fit = [None] * N

# INITIALISE FLIES WITHIN BOUNDS
for i in range(N):
    for d in range(D):
        X[i, d] = np.random.uniform(lowerB[d], upperB[d])

# MAIN DFO LOOP
for itr in range(maxIterations):
    ax = plt.subplot()
    ax.scatter(x_coor, y_coor, color='b', marker='^')
    plt.draw()
    plt.show(block=False)

    for i in range(N):  # EVALUATION
        fitness[i] = f(X[i,])
        # print(fitness, "fit")
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
        bNeighbour = right if fitness[right] < fitness[left] else left

        for d in range(D):  # UPDATE EACH DIMENSION SEPARATELY
            if np.random.rand() < delta:
                X[i, d] = np.random.uniform(lowerB[d], upperB[d])
                continue;

        # for j in range(N):
        #     fit[j] = f(X[j,])
        #     for a in fit:
        #         print(a, "a")

            u = np.random.rand()
            X[i, d] = X[bNeighbour, d] + u * (X[bNeighbour, d] - X[i, d])

            # OUT OF BOUND CONTROL
            if X[i, d] < lowerB[d] or X[i, d] > upperB[d]:
                X[i, d] = np.random.uniform(lowerB[d], upperB[d])

    rowNo = X[s, 0]
    colNo = X[s, 1]
    swarmBestCircle = plt.Circle((rowNo, colNo), 10, color='r')
    # COVERAGE RADIUS FOR THE DRONES IN THE PLOT
    cir = plt.Circle((rowNo, colNo), R, color='y', fill=False)
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
        cir = plt.Circle((X[i, 0], X[i, 1]), R, color='y', fill=False)
        ax.set_aspect('equal', adjustable='datalim')
        ax.add_patch(cir)

    plt.gca().add_patch(swarmBestCircle)  # ADD THE CIRCLE
    plt.draw()  # DRAW THE IMAGE AND THE CIRCLE
    plt.show(block=False)
    plt.pause(0.01)
    plt.clf()

for i in range(N): fitness[i] = f(X[i,])  # EVALUATION
s = np.argmax(fitness)  # FIND BEST FLY

print("\nFinal best fitness:\t", fitness[s])
print("\nBest fly position:\n", X[s,])
