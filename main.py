import math
import numpy as np
import matplotlib.pyplot as plt

# Randomizing the x and y coordinates
x = np.random.randint(0, 89, size=20)
y = np.random.randint(0, 89, size=20)

ax = plt.subplot()

# Plot labels and plot type
ax.scatter(x, y, color='b', marker='^')
plt.xlabel("x")
plt.ylabel("y")


# User Coordinates
coordinates = []
for i, j in zip(x, y):
    coordinates.append((i, j))

# Saving the coordinates to a txt file
file = open('coordinates.txt', 'w')
for items in coordinates:
    line = ' '.join(str(x) for x in items)
    file.write(line + '\n')

file.close()



# Parameters
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

imgW = 10
imgH = 5


# FITNESS FUNCTION
# PL_th(Pathloss Threshold) is the x
def f(x):  # x IS A VECTOR REPRESENTING ONE FLY
    R = 0.0
    for i in range(len(x)):
        R = (-(20 * A_1) / (1 + a * math.exp(-b * (((180 / math.pi) * thita_opt) - a))) - (B_1 / 20) + (
                x[0] / 20)) * math.cos(thita_opt)
    return R


N = 10 # POPULATION SIZE
D = 2  # DIMENSIONALITY
delta = 0.001  # DISTURBANCE THRESHOLD
maxIterations = 500  # ITERATIONS ALLOWED

# DC_Pathloss
lowerB = [0, 0]  # LOWER BOUND (IN ALL DIMENSIONS)
upperB = [89, 89]  # UPPER BOUND (IN ALL DIMENSIONS)

# INITIALISATION PHASE
X = np.empty([N, D])  # EMPTY FLIES ARRAY OF SIZE: (N,D)
fitness = [None] * N  # EMPTY FITNESS ARRAY OF SIZE N

# INITIALISE FLIES WITHIN BOUNDS
for i in range(N):
    for d in range(D):
        X[i, d] = np.random.uniform(lowerB[d], upperB[d])

# MAIN DFO LOOP
for itr in range(maxIterations):
    for i in range(N):  # EVALUATION
        fitness[i] = f(X[i,])
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
                X[i, d] = np.random.uniform(lowerB[d], upperB[d])
                continue;

            u = np.random.rand()
            X[i, d] = X[bNeighbour, d] + u * (X[s, d] - X[i, d])

            # OUT OF BOUND CONTROL
            if X[i, d] < lowerB[d] or X[i, d] > upperB[d]:
                X[i, d] = np.random.uniform(lowerB[d], upperB[d])

    rowNo = X[s, 1]
    colNo = X[s, 0]
    swarmBestCircle = plt.Circle((rowNo, colNo), 1, color='r')
    # Coverage Range of the Drones
    cir = plt.Circle((rowNo, colNo), 10, color='b', fill=False)
    ax.set_aspect('equal', adjustable='datalim')
    ax.add_patch(cir)

    # for a, b in zip(rowNo,colNo):
    #     print(a,b)

    circle = []  # THIS SECTION IS OPTIONAL TO SHOW ALL FLIES
    for i in range(N):
        circle.append(plt.Circle((X[i, 1], X[i, 0]), 1, color='g'))
        plt.gca().add_patch(circle[i])
        # Coverage Radius of the Drones
        cir = plt.Circle((X[i,1], X[i,0]), 10, color='b', fill=False)
        ax.set_aspect('equal', adjustable='datalim')
        ax.add_patch(cir)

    plt.gca().add_patch(swarmBestCircle)  # ADD THE CIRCLE
    plt.show(block = False)
    plt.draw()  # DRAW THE IMAGE AND THE CIRCLE # REMOVE THE AXES
    plt.pause(0.01) # PAUSE BEFORE THE NEXT ITERATION IN BETWEEN
    # plt.clf()  # CLEAR THE CANVAS
    # ax.grid(True)


for i in range(N): fitness[i] = f(X[i,])  # EVALUATION
s = np.argmax(fitness)

# FIND BEST FLY
print("\nFinal best fitness:\t", fitness[s])
print("\nBest fly position:\n", X[s,])
print("\nTotal circumference:\n", 2 * math.pi * fitness[s])
print("\nHeight:\n", fitness[s] * math.tan(thita_opt))

