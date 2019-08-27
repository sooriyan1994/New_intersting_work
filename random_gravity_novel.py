import numpy
import matplotlib.pyplot as plt
import time
import random


def distance(X,Y):
    '''calculates the distance between two coordinate points'''

    dis = numpy.sqrt((X[0]-Y[0])**2+(X[1]-Y[1])**2)
    return round(dis,4)


def minimum_distance(coords, i):
    '''minimum distance between one coordinate point and the rest of all coordinate points'''

    minimum = max(coords[:,0])
    for j in numpy.delete(range(len(coords)), i):
        if distance(coords[i], coords[j]) <= minimum:
            minimum = distance(coords[i], coords[j])
    return minimum


# TO check the execution time of the program
start = time.time()

##d = int(input("Enter the diameter of the fibre (in microns): "))
d = 6
A_f = numpy.pi * d**2 /4 # area occupied by each fiber
##a = int(input("Side of the square area to be filled: "))
a = 60
A = a**2 # Area of the square area

dis = 0.1 #Distance betweeen two fibers
mag = d + dis # Minimum Distance between two fiber centers

##V_f = float(input("Preferred Volume fraction: "))
V_f = 0.5

n = int(V_f * A/A_f)
print('Number of fibers to be filled in the area : ', n)

dist_border = 0.1 # distance b/w the edge and the edge of fiber

no_iters = 250

#Discretising the square area
x = numpy.linspace(dist_border+d/2, a-(dist_border+d/2), 600, dtype=numpy.float)
y = numpy.linspace(dist_border+d/2, a-(dist_border+d/2), 600, dtype=numpy.float)

space = numpy.stack(numpy.meshgrid(x, y), -1).reshape(-1,2)

#choosing the required number of fibers from the discretised square area
coords = numpy.array([])
index = random.sample(range(len(space)),n)
for i in range(len(index)):
    coords = numpy.append(coords, space[index[i]]).reshape(-1,2)

plt.figure(figsize=(10,10))
plt.scatter(coords[:,0], coords[:,1], s=3)

#calculating the distance between points
x_fix = ((numpy.argmin(coords)+1)/2) - 1
y_fix = numpy.argmin(coords) % 2

for k in range(250):
    for i in range(n):
        active = [x_fix]
        for j in numpy.delete(range(n),i):
            r = distance(coords[i], coords[j])
            if r <= mag:
                force = 4 * 0.01 * ( (6.1/r)**12 - (6.1/r)**6 )
                if force > 10:
                    force = 10
                theta = numpy.arctan((coords[j][1] - coords[i][1])/(coords[j][0] - coords[i][0]))
                coords[j] = coords[j][0] + force*numpy.cos(theta), coords[j][1] + force*numpy.sin(theta)
            
            
##    for j in range(n):
##        if j != i:
##            distance = (coords[i][0] - coords[j][0])**2 + (coords[i][1] - coords[j][1])**2
##            if distance < mag:
##                delta = (mag - distance)
##                unit_x = (coords[i][0] - coords[j][0]) / distance
##                unit_y = (coords[i][1] - coords[j][1]) / distance
##                coords[i][0] = coords[i][0] + delta * unit_x
##                coords[i][1] = coords[i][1] + delta * unit_y
##
##        if j == n-1:
##            for 
            
#plot
#plt.figure(figsize=(10,10))
plt.scatter(coords[:,0], coords[:,1], s=3)
plt.axis([0, 60, 0, 60])
plt.show()

plt.figure(figsize=(10,10))
plt.scatter(coords[:,0], coords[:,1], s=3)
plt.show()
