# IMPORTING THE LIBRARIES
import csv
import math
import numpy as np
import matplotlib.pyplot as plt

# EXPERIMENTAL PARAMETERS BASED ON THE SUB-URBAN ENVIRONMENT
thita_opt = 0.35499997  # OPTIMAL ELEVATION ANGLE
a = 4.88  # CONSTANT VALUE
b = 0.43  # CONSTANT VALUE # CONSTANT VALUE
P_LoS = 0.1  # PROBABILITY OF LINE OF SIGHT
P_NLoS = 21  # PROBABILITY OF NON LINE OF SIGHT
f_c = 5000  # CARRIER FREQUENCY
c = 299792458  # SPEED OF LIGHT
A_1 = P_LoS - P_NLoS
B_1 = 20 * math.log10((4 * math.pi * f_c) / c) + P_LoS
alpha = 3.04
A = -23.29
thita_zero = -0.05515240
B = 4.14
n_zero = 20.7
covud = []
cov = []


coordinates = []  # ARRAY TO STORE THE USER COORDINATES

''' GENERATE NEW COORDINATES EACH RUN  '''
# RANDOM INITIALIZATIONS OF THE USER COORDINATES
x_coor = np.random.randint(0, 3000, size=20)
y_coor = np.random.randint(0, 3000, size=20)
bs_xcoor = 1500
bs_ycoor = 1500

for i, j in zip(x_coor, y_coor):
    coordinates.append((i, j))

with open('coordinates.csv', 'w', newline='') as file:
    mywriter = csv.writer(file, delimiter=',')
    mywriter.writerows(coordinates)

# ''' USE SAVED COORDINATES '''
# coor = np.genfromtxt('cov_users.csv', delimiter=',')
# for i, j in coor:
#     coordinates.append((i, j))


# FITNESS FUNCTION
def f(x):  # x IS THE COORDINATED OF ONE FLY
    DUB = 0
    yes = 0
    for items in coordinates:
        x_i = items[0]  # USER X COORDINATE
        y_i = items[1]  # USER Y COORDINATE
        for i in range(N):
            x_d = x[0]  # FLY/DRONE X COORDINATE
            y_d = x[1]  # FLY/DRONE Y COORDINATE
            R = radius[i]  # FLY/DRONE COVERAGE RADIUS
            # CHECKING IF THE USER IS WITHIN THE COVERAGE RADIUS OF THE DRONE/FLY
            coverage = ((x_i - x_d) ** 2 + (y_i - y_d) ** 2)
            # IF USER USER WITHIN THE COVERAGE RADIUS COUNTER INCREMENT BY 1
            if coverage <= R * R +5:
                yes += 1
    for i in range(N):
        x_d = x[0]  # FLY/DRONE X COORDINATE
        y_d = x[1]  # FLY/DRONE Y COORDINATE
        r_db = math.sqrt((x_d - bs_xcoor) ** 2 + (y_d - bs_ycoor) ** 2)
        # r_db = math.sqrt((bs_xcoor - x_d) ** 2 + (bs_ycoor - y_d) ** 2)
        DUB = 10 * alpha * math.log(r_db) + \
              A*(thita_opt - thita_zero) ** (thita_zero - thita_opt / B) + n_zero
    # print(DUB,"dub pathloss")
    # print(r_db,"drone to base range")
    return yes / 20


# COVERAGE RADIUS FUNCTION
def rad(x):  # X IS THE PATHLOSS OF ONE FLY
    r = 0.0
    for i in range(len(x)):
        # FINDING THE COVERAGE RADIUS OF EACH DONE IN ACCORDANCE WITH THE PATHLOSS VALUE
        r = (-(20 * A_1) / (1 + a * math.exp(-b * (((180 / math.pi) * thita_opt) - a))) - (B_1 / 20) + (
                x[2] / 20)) * math.cos(thita_opt)
    return r


N = 20  # POPULATION SIZE
D = 3  # DIMENSIONALITY
delta = 0.005  # DISTURBANCE THRESHOLD
maxIterations = 1000  # ITERATIONS ALLOWED
lowerB = [0, 0, 0]  # LOWER BOUND (IN ALL DIMENSIONS)
upperB = [3000, 3000, 100]  # UPPER BOUND (IN ALL DIMENSIONS)

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

# HEIGHT OF EACH FLY/DRONE IN ACCORDANCE WITH COVERAGE RADIUS
for y in radius:
    h = y * math.tan(thita_opt)
    height.append(h)

while len(coordinates) != 0:
    # MAIN DFO LOOP
    for itr in range(1, maxIterations):
        ax = plt.subplot()
        # USER COORDINATES FOR PLOTTING
        for i, j in coordinates:
            x = i
            y = j
            ax.scatter(x, y, color='b', marker=',')
            ax.scatter(bs_xcoor,bs_ycoor, color='r', marker='^')
        plt.draw()
        plt.show(block=False)

        for i in range(N):  # EVALUATION
            fitness[i] = f(X[i,])
        s = np.argmax(fitness)  # FIND BEST FLY

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

        if itr % 100 == 0:  # PRINT BEST FLY EVERY 100 ITERATIONS
            print("Iteration:", itr, "\tBest fly index:", s, "\tFitness", fitness[s])
            for it in coordinates:
                x_i = it[0]  # USER X COORDINATE
                y_i = it[1]  # USER Y COORDINATE
                x_d = X[s, 0]  # DRONE/FLY X COORDINATE
                y_d = X[s, 1]  # DRONE/FLU Y COORDINATE
                R = radius[s]
                coverage = ((x_i - x_d) ** 2 + (y_i - y_d) ** 2)
                if coverage <= R * R and fitness[s] >= 2 :
                    # IF USER WITHIN THE DRONE COVERAGE RADIUS APPEND THE DRONE AND THE COVERED USERS
                    covud.append(((x_d, y_d, height[s], radius[s]), (x_i, y_i)))
                    # STORING THE COVERED USERS IN AN ARRAY FOR LATER USE
                    cov.append((x_i, y_i))
                    print(x_i,y_i,"users")
                    # REMOVE THE COVERED USERS FROM THE USER COORDINATES ARRAY
                    coordinates.remove((x_i, y_i))

            # with open('cov_users.csv', 'w', newline='') as f:
            #     mw = csv.writer(f, delimiter=',')
            #     mw.writerows(cov)

            d = {}
            for x in covud:
                # STORING THE COORDINATED IN A DICTIONARY WHERE THE BEST DRONE IS THE KEY
                # AND THE COVERED USERS IS THE VALUES
                d.setdefault(x[0], []).append(x[1])
            # SAVING THE COVERED USERS AND TEH ASSOCIATED DRONE IN A TEXT FILE
            with open('coverage.txt', 'w') as fw:
                fw.write(str(d))

            # for key, value in d.items():
            #     # for i in value:
            #     print(value,"test")
            with open('cov_users.csv', 'w', newline='') as file:
                mywriter = csv.writer(file, delimiter=',')
                mywriter.writerows(cov)

            # SAVING THE BEST DRONE COORDINATES, HEIGHT AND RADIUS TO A CSV FILE
            with open('best_drones.csv', 'w', newline='') as file:
                mywriter = csv.writer(file, delimiter=',')
                mywriter.writerows(d)

        # PLOTTING THE BEST FLY
        rowNo = X[s, 0]  # BEST FLY X COORDINATE
        colNo = X[s, 1]  # BEST FLY Y COORDINATE
        swarmBestCircle = plt.Circle((rowNo, colNo), 10, color='r')
        # COVERAGE RADIUS FOR THE BEST DRONES IN THE PLOT
        cir = plt.Circle((rowNo, colNo), radius[s], color='y', fill=False)
        ax.set_aspect('equal', adjustable='datalim')
        ax.add_patch(cir)

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
    break

# FINDING THE UNCOVERED USERS
f1 = open('coordinates.csv', 'r', newline='')
f2 = open('cov_users.csv', 'r', newline='')
f3 = open('ucov_users.csv', 'w', newline='')
c1 = csv.reader(f1)
c2 = csv.reader(f2)
c3 = csv.writer(f3)
masterlist = [row[0] for row in c2]

for hosts_row in c1:
    if hosts_row[0] not in masterlist:
        c3.writerow(hosts_row)
