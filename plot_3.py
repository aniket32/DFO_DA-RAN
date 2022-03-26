import csv
coordinates = []

with open("coordinates.csv", "r") as f:
    wr = csv.reader(f)
    for row in wr:
        x_coor = int(row[0])
        y_coor = int(row[1])
        coordinates.append((x_coor,y_coor))

