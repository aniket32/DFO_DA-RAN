# IMPORTING THE LIBRARIES
import csv
import math
import numpy as np
import matplotlib.pyplot as plt

# RANDOM INITIALIZATIONS OF THE USER COORDINATES
x_coor = np.random.randint(1000, 4000, size=20)
y_coor = np.random.randint(1000, 4000, size=20)

# LIMITS FOR THE PLOT
x_limit = 5000
y_limit = 5000

# BASE STATION COORDINATES TO BE IN THE CENTRE OF THE PLOT
bs_xcoor = x_limit / 2
bs_ycoor = y_limit / 2

# EXPERIMENTAL PARAMETERS BASED ON THE SUB-URBAN ENVIRONMENT
a = 4.88  # CONSTANT VALUE
b = 0.43  # CONSTANT VALUE
A = -23.29  # CONSTANT VALUE
B = 4.14  # CONSTANT VALUE
f_c = 2400  # CARRIER FREQUENCY
c = 299792458  # SPEED OF LIGHT
alpha = 3.04  # CONSTANT VALUE
nLoS = 0.1  # MEAN ADDITIONAL LOSS FOR LINE OF SIGHT
nNLoS = 21  # MEAN ADDITIONAL LOS FOR NON LINE OF SIGHT
n_zero = 20.7  # CONSTANT VALUE
thita_zero = -3.61  # CONSTANT VALUE
thita_opt = 0.35499997  # OPTIMAL ELEVATION ANGLE
PL_D2U_max = 89  # UPPERBOUND FOR USER TO DRONE PATHLOSS
PL_D2U_min = 0  # LOWER BOUND FOR USER TO DRONE PATHLOSS
PL_D2B_max = 80  # UPPERBOUND FOR DRONE TO BASE STATION PATHLOSS
PL_D2B_min = 0  # UPPERBOUND FOR DRONE TO BASE STATION PATHLOSS
A_1 = nLoS - nNLoS  # PARAMETER FOR COVERAGE RADIUS
B_1 = 20 * math.log10((4 * math.pi * f_c) / c) + nLoS  # PARAMETER FOR COVERAGE RADIUS
H = 200  # HEIGHT OF THE BASE STATION
# MAX RANGE FROM DRONE TO BASE STATION
total_r_db = 1280
max_R_DB = total_r_db + 400  # TOTAL OPERATIONAL RANGE OF DRONES
# FINDING THE MAXIMUM COVERAGE RADIUS OF DRONES WHEN THE THITA_OPT AND PATHLOSS THRESHOLD IS KNOWN
r = (-(20 * A_1) / (1 + pow(a, (-b * (((180 / math.pi) * thita_opt) - a)))) - (B_1 / 20) +
     (PL_D2U_max / 20)) * math.cos(thita_opt)
h = r * math.tan(thita_opt)  # HEIGHT OF THE DRONES

# effect of variation in plot and pathloss values
# mention D2B challenges and results
# chain drone (cloud)


N = 20  # POPULATION SIZE
D = 2  # DIMENSIONALITY
delta = 0.001  # DISTURBANCE THRESHOLD
maxIterations = 2600  # ITERATIONS ALLOWED

lowerB = [1000, 1000]  # LOWER BOUND (IN ALL DIMENSIONS)
upperB = [4000, 4000]  # UPPER BOUND (IN ALL DIMENSIONS)

# INITIALISATION PHASE
X = np.empty([N, D])  # EMPTY FLIES ARRAY OF SIZE: (N,D)
fitness = [None] * N  # EMPTY FITNESS ARRAY OF SIZE N
coordinates = []  # ARRAY TO STORE THE USER COORDINATES
cov = []  # COVERED USERS ARRAY
cov_ud = []  # COVERED USERS AND ASSOCIATED DRONES ARRAY
bd = [(0, 0)]  # BEST DRONE COORDINATE ARRAY
r_dd = [] * len(bd)  # DISTANCE BETWEEN BEST DRONES ARRAY

# INITIALISE FLIES WITHIN BOUNDS
for i in range(N):
    for d in range(D):
        X[i, d] = np.random.uniform(lowerB[d], upperB[d])

# STORING THE USER COORDINATES IN AN ARRAY
for i, j in zip(x_coor, y_coor):
    coordinates.append((i, j))

# SAVING ALL THE USER COORDINATES IN A CSV FILE
with open('coordinates.csv', 'w', newline='') as file:
    mw = csv.writer(file, delimiter=',')
    mw.writerows(coordinates)


# FIND THE MAX OPERATIONAL RANGE OF THE DRONE
# THE TOTAL MAX OPERATIONAL RANGE WILL BE R_DB + HALF OF THE COVERAGE OF DRONE
# THE TOTAL OPERATIONAL RANGE IS SHOWN BY THE RED CIRCLE IN THE PLOT
# USED FOR TESTING AND NOT EACH TIME DURING COMPILATION
def D2B_pathloss(x):  # x IS A VECTOR REPRESENTING ONE FLY COORDINATES
    R_DB = []
    for i in range(N):
        x_d = x[0]  # DRONE X COORDINATE
        y_d = x[1]  # DRONE Y COORDINATE
        # ANGLE BETWEEN DC AND BS
        # NOT NECESSARY, SINCE IT IS TAKEN INTO ASSUMPTION THAT THE ANGLE IS ZERO FOR BEST PATHLOSS VALUES
        thita = math.atan2(((bs_xcoor - x_d) ** 2), ((bs_ycoor - y_d) ** 2)) * (180 / math.pi)
        # DISTANCE BETWEEN DRONE AND BASE STATION
        r_db = math.sqrt((bs_xcoor - x_d) ** 2 + (bs_ycoor - y_d) ** 2)
        # DRONE TO BASE PATHLOSS
        PL = 10 * alpha * math.log10(r_db) + A * ((0 - thita_zero) * math.exp((thita_zero - 0) / B)) + n_zero
        # CHECKING IF THE PATHLOSS IS WITHIN THE PATHLOSS THRESHOLD
        # IF PATHLOSS IS WITH THE BOUNDS RETURN THE MAX DISTANCE
        if PL <= PL_D2B_max:
            R_DB.append(r_db)
    return R_DB


# FITNESS FUNCTION
def f(x):  # x IS A VECTOR REPRESENTING ONE FLY COORDINATES
    yes = 0
    for items in coordinates:
        x_i = items[0]  # USER X COORDINATE
        y_i = items[1]  # USER Y COORDINATE
        for j in range(N):
            x_d = x[0]  # FLY/DRONE X COORDINATE
            y_d = x[1]  # FLY/DRONE Y COORDINATE
            # DISTANCE BETWEEN THE DRONE AND THE USER
            coverage = ((x_i - x_d) ** 2 + (y_i - y_d) ** 2)
            # DISTANCE BETWEEN DRONE AND BASE STATION
            r_db = math.sqrt((bs_xcoor - x_d) ** 2 + (bs_ycoor - y_d) ** 2)
            # FINDING THE MAX ALLOWED DISTANCE FROM DRONE TO BASE STATION
            if coverage <= r * r and r_db <= total_r_db:
                # INCREMENTING IF CONDITIONS SATISFY
                yes += 1
    # RETURNS THE NUMBER OF USERS COVERED BY A DRONE/FLY
    return yes / N


def range_test(x):
    no = 0
    for k in x:
        if 800 > k > 0:
            no += 1
    return no


# MAIN DFO LOOP
for itr in range(1, maxIterations):
    ax = plt.subplot()
    # PLOTTING THE BASE STATION
    ax.scatter(bs_xcoor, bs_ycoor, color='r', marker='^')
    # PLOTTING THE BASE STATION COVERAGE RANGE
    cir = plt.Circle((bs_xcoor, bs_ycoor), 2500, color='y', fill=False)
    ax.set_aspect('equal', adjustable='datalim')
    # PLOTTING THE OPERATIONAL RANGE OF DRONES
    c = plt.Circle((bs_xcoor, bs_ycoor), max_R_DB, color='r', fill=False)
    ax.set_aspect('equal', adjustable='datalim')
    ax.add_patch(cir)
    ax.add_patch(c)

    # PLOTTING THE USERS
    for i, j in coordinates:
        x = i  # USER X COORDINATE
        y = j  # USER Y COORDINATE
        ax.scatter(x, y, color='b', marker=',')
    plt.draw()
    plt.show(block=False)

    for i in range(N):  # EVALUATION
        fitness[i] = f(X[i,])
        # FIND BEST FLY
        # THE DRONE/FLY WITH THE MAXIMUM NUMBER OF USERS IS THE BEST FLY
    s = np.argmax(fitness)

    if itr % 150 == 0:
        # AFTER EVERY 150 ITERATIONS
        print("Iteration:", itr, "\tUsers covered:", fitness[s])
        # STORING THE CURRENT BEST FLY X AND Y COORDINATES
        bd.append((X[s, 0], X[s, 1]))
        x_d = X[s, 0]  # CURRENT BEST FLY/DRONE X COORDINATE
        y_d = X[s, 1]  # CURRENT BEST FLY/DRONE Y COORDINATE
        for j, k in bd:
            x_coor = j  # PREVIOUS BEST FLY/DRONE Y COORDINATE
            y_coor = k  # PREVIOUS BEST FLY/DRONE Y COORDINATE
            ran = math.sqrt((x_d - x_coor) ** 2 + (y_d - y_coor) ** 2)
            # SAVING THE DISTANCE BETWEEN CURRENT AND PREVIOUS BEST DRONE
            r_dd.append(ran)

        if range_test(r_dd) >= 1:
            for i in range(N):
                for d in range(D):  # UPDATE EACH DIMENSION SEPARATELY
                    X[i, d] = np.random.uniform(lowerB[d], upperB[d])
        elif range_test(r_dd) == 0:
            for i in range(N):
                for it in coordinates:
                    x_i = it[0]  # USER X COORDINATE
                    y_i = it[1]  # USER Y COORDINATE
                    x_d = X[s, 0]  # DRONE/FLY X COORDINATE
                    y_d = X[s, 1]  # DRONE/FLU Y COORDINATE
                    # DRONE COVERAGE
                    coverage = ((x_i - x_d) ** 2 + (y_i - y_d) ** 2)
                    # DRONE TO BASE STATION DISTANCE
                    r_db = math.sqrt((bs_xcoor - x_d) ** 2 + (bs_ycoor - y_d) ** 2)
                    if coverage <= r * r and r_db <= 1280:
                        # SAVING COVERED USERS AND ASSOCIATED DRONE
                        cov_ud.append(((x_d, y_d, h), (x_i, y_i)))
                        # SAVING COVERED USERS
                        cov.append((x_i, y_i))
                        # REMOVING THE COVERED FROM THE SEARCH SPACE
                        coordinates.remove((x_i, y_i))
    # CLEARING THE ARRAY FOR NEXT ITERATION
    r_dd.clear()

    # STORING THE COORDINATES
    d = {}
    for x in cov_ud:
        # STORING THE COORDINATED IN A DICTIONARY WHERE THE BEST DRONE IS THE KEY
        # AND THE COVERED USERS IS THE VALUES
        d.setdefault(x[0], []).append(x[1])
    # SAVING THE COVERED USERS AND TEH ASSOCIATED DRONE IN A TEXT FILE
    with open('coverage.txt', 'w') as fw:
        fw.write(str(d))

    # SAVING THE COVERED USERS IN A CSV FILE
    with open('cov_users.csv', 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(cov)

    # SAVING THE BEST DRONE COORDINATES, HEIGHT AND RADIUS TO A CSV FILE
    with open('best_drones.csv', 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(d)

    # TAKE EACH FLY INDIVIDUALLY
    for i in range(N):
        if i == s: continue  # ELITIST STRATEGY

        # FIND BEST NEIGHBOUR
        left = (i - 1) % N
        right = (i + 1) % N
        bNeighbour = right if fitness[right] < fitness[left] else left

        for d in range(D):  # UPDATE EACH DIMENSION SEPARATELY
            if np.random.rand() < delta or range_test(r_dd) >= 1:
                X[i, d] = np.random.uniform(lowerB[d], upperB[d])
                continue

            u = np.random.rand()
            X[i, d] = X[bNeighbour, d] + u * (X[bNeighbour, d] - X[i, d])

            # OUT OF BOUND CONTROL
            if X[i, d] < lowerB[d] or X[i, d] > upperB[d]:
                X[i, d] = np.random.uniform(lowerB[d], upperB[d])

    # PLOTTING
    x_d = X[s, 0]  # DRONE X COORDINATE
    y_d = X[s, 1]  # DRONE Y COORDINATE
    swarmBestCircle = plt.Circle((x_d, y_d), 15, color='r')
    # PLOTTING THE COVERAGE RADIUS OF THE BEST DRONE
    cir = plt.Circle((x_d, y_d), r, color='y', fill=False)
    ax.set_aspect('equal', adjustable='datalim')
    ax.add_patch(cir)

    circle = []  # THIS SECTION IS OPTIONAL TO SHOW ALL FLIES
    for i in range(N):
        circle.append(plt.Circle((X[i, 0], X[i, 1]), 10, color='g'))
        plt.gca().add_patch(circle[i])
        # PLOTTING THE COVERAGE OF ALL DRONES
        cir = plt.Circle((x_d, y_d), r, color='y', fill=False)
        ax.set_aspect('equal', adjustable='datalim')
        ax.add_patch(cir)

    plt.gca().add_patch(swarmBestCircle)  # ADD THE CIRCLE
    plt.draw()  # PLOTTING THE PLOT AND THE CIRCLES
    plt.xlim([0, x_limit])  # LIMITING THE PLOT IN X ASIS
    plt.ylim([0, y_limit])  # LIMITING THE PLOT IN Y ASIS
    plt.show(block=False)
    plt.pause(0.01)  # PAUSE BEFORE THE NEXT ITERATION IN BETWEEN
    plt.clf()  # CLEAR THE CANVAS

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

f1.close()
f2.close()
f3.close()
