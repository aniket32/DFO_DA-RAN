import math

import numpy as np

thita_opt = 0.35499997
a = 4.88
b = 0.43
A = -23.39
B = 4.14
P_LoS = 0.1
P_NLoS = 21
f_c = 2.4
c = 300
A_1 = P_LoS - P_NLoS
B_1 = 20 * math.log10((4 * math.pi * f_c) / c) + P_LoS


# FITNESS FUNCTION
# PL_th(Pathloss Threshold) is the x
def f(x):  # x IS A VECTOR REPRESENTING ONE FLY
    R = 0.0
    for i in range(len(x)):
        R = (-(20 * A_1) / (1 + a * math.exp(-b * (((180 / math.pi) * thita_opt) - a))) - (B_1 / 20) + (
                x[0] / 20)) * math.cos(thita_opt)
    return R


N = 500  # POPULATION SIZE
D = 1  # DIMENSIONALITY
delta = 0.001  # DISTURBANCE THRESHOLD
maxIterations = 1000  # ITERATIONS ALLOWED

# DC_Pathloss
lowerB = [0]  # LOWER BOUND (IN ALL DIMENSIONS)
upperB = [89]  # UPPER BOUND (IN ALL DIMENSIONS)

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
    s = np.argmin(fitness)  # FIND BEST FLY

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
            X[i, d] = X[bNeighbour, d] + u * (X[bNeighbour, d] - X[i, d])

            # OUT OF BOUND CONTROL
            if X[i, d] < lowerB[d] or X[i, d] > upperB[d]:
                X[i, d] = np.random.uniform(lowerB[d], upperB[d])

for i in range(N): fitness[i] = f(X[i,])  # EVALUATION
s = np.argmax(fitness)  # FIND BEST FLY

print("\nFinal best fitness:\t", fitness[s])
print("\nBest fly position:\n", X[s,])
print("\nTotal circumference:\n", 2 * math.pi * fitness[s])
print("\nHeight:\n", fitness[s] * math.tan(thita_opt))
