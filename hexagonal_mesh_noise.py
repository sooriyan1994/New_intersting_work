import numpy
import matplotlib.pyplot as plt
import time

'''Creates a regularly spaced hexagonal package of circles. The hexagonal array is disturbed by first crisscrossing them.
    Then locally disturb them by finding the maximum movable distance by calculating the distance of the nearest
    neighbour. '''

#To calculate the time for execution of the program
start = time.time()

def minimum_distance(coords, i):
    '''minimum distance between one coordinate point and the rest of all coordinate points'''

    minimum = max(coords[:,0])
    for j in numpy.delete(range(len(coords)), i):
        if distance(coords[i], coords[j]) <= minimum:
            minimum = distance(coords[i], coords[j])
    return minimum


def distance(X,Y):
    '''calculates the distance between two coordinate points'''

    dis = numpy.sqrt((X[0]-Y[0])**2+(X[1]-Y[1])**2)
    return round(dis,4)


#Diameter of fiber
d = 6 #in mm
#Area of one fiber
A_f = (numpy.pi * d**2)/4

#Dimensions of the square are that are to be filled out
a = 60 #side of square(in mm)
A = a**2

#Distance betweeen two fibers
dis = 0.1
# Minimum Distance between two fiber centers
min_dist = d + dis 

##V_f = float(input("Preferred Volume fraction: "))
V_f = 0.7

# Number fo fibers to be filled for the corresponding volume fractio
n = int((V_f * A)/A_f)
print('Number of fibers to be filled in the area : ', n)
#Number of iterations for Wongsto, Li algorithm
no_iter = 250

# compute grid shape based on number of points
num_y = numpy.int(numpy.sqrt(n/2) + 1)
num_x = numpy.int(n / (2 * num_y) + 1)

dist_border = 0.1 # distance b/w the edge and the edge of fiber

eq_dis = (a - num_x * d - 2 * dist_border)/(num_x + 1)

# create regularly spaced neurons
x_s = numpy.linspace(max(eq_dis,(d/2 + dist_border)), a - max(eq_dis,(d/2 + dist_border)), num_x, dtype=numpy.float)
y_s = numpy.linspace(max(eq_dis,(d/2 + dist_border)), a - max(eq_dis,(d/2 + dist_border)), num_y, dtype=numpy.float)
#coords = numpy.stack(numpy.meshgrid(x_s, y_s), -1).reshape(-1,2) #-1 simply means that it is an unknown dimension

#creating hexagonal packing
x_t = numpy.arange(x_s[0] + (x_s[1]- x_s[0])/2 , a-(dist_border + d/2), x_s[1]-x_s[0], dtype=numpy.float)
y_t = numpy.arange(y_s[0] + (y_s[1]- y_s[0])/2, a-(dist_border + d/2), y_s[1]-y_s[0], dtype=numpy.float)

#Packing hexagonal mesh
coords = numpy.append(numpy.dstack(numpy.meshgrid(x_s, y_s)), numpy.dstack(numpy.meshgrid(x_t, y_t))).reshape(-1,2)

# compute spacing
init_dist = numpy.sqrt((x_t[0]-x_s[0])**2+(y_t[0]-y_s[1])**2)
#checking if the fiber arrangement confers to the requirement
assert init_dist >= min_dist, "Too many fibers, cant fill these many number of fibers"

# perturb points
for no_it in range(no_iter):
    for i in range(len(coords)):
        rho = numpy.random.uniform(0, minimum_distance(coords,i)-min_dist)
        while True:
            theta = numpy.random.uniform(0, 2*numpy.pi)
            if (d/2 + dist_border) <= (coords[i][0] + rho*numpy.cos(theta)) <=  a-(dist_border + d/2) and \
               (d/2 + dist_border) <= (coords[i][1] + rho*numpy.sin(theta)) <=  a-(dist_border + d/2):
                coords[i] = coords[i][0] + rho*numpy.cos(theta), coords[i][1] + rho*numpy.sin(theta)
                break
            else:
                for j in range(10):
                    theta = theta + numpy.random.uniform(0, numpy.pi)
                    if (d/2 + dist_border) <= (coords[i][0] + rho*numpy.cos(theta)) <=  a-(dist_border + d/2) and \
                       (d/2 + dist_border) <= (coords[i][1] + rho*numpy.sin(theta)) <=  a-(dist_border + d/2):
                        coords[i] = coords[i][0] + rho*numpy.cos(theta), coords[i][1] + rho*numpy.sin(theta)
                        break
                break       


#Time for execution
stop = time.time()
print(stop-start)

#Uncomment it to check if all fibers are sufficiently away from others
#for i in range(len(coords)):
#    print(minimum_distance(coords, i))

# plot
#plt.figure(figsize=(10,10))
#plt.scatter(coords[:,0], coords[:,1], s=3)
#plt.show()
